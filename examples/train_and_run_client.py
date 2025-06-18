import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from datasets import load_dataset
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from cifer import CiferClient  # ตรวจให้แน่ใจว่าติดตั้งผ่าน pip install cifer แล้ว

# === 📦 Dataset Config ===
dataset_hf_id = "CiferAI/Cifer-Fraud-Detection-Dataset-AF"
dataset_csv_path = "./datasets/Cifer-Fraud-Detection-Dataset-AF.csv"
dataset_npz_path = "./datasets/Cifer-Fraud-Detection-Dataset-AF.npz"
model_path = "./trained_model/fraud_model.h5"

# === 📥 Load Dataset from HuggingFace ===
print("📥 Loading dataset ...")
ds = load_dataset(dataset_hf_id)
df = ds["train"].to_pandas()

# ✅ Optional: reduce data size for faster training
df = df.sample(n=100_000, random_state=42)

# 💾 Save CSV
os.makedirs(os.path.dirname(dataset_csv_path), exist_ok=True)
df.to_csv(dataset_csv_path, index=False)

# === 🧹 Preprocessing ===
df_clean = df.apply(pd.to_numeric, errors="coerce").fillna(0)
X = df_clean.iloc[:, :-1].astype(np.float32).to_numpy()
y = df_clean.iloc[:, -1]

if y.dtype == "object" or y.nunique() > 2:
    y = LabelEncoder().fit_transform(y)
else:
    y = y.astype(np.int32)
y = np.array(y).reshape(-1,)

print(f"✅ Feature shape: {X.shape}, Label shape: {y.shape}")

# 💾 Save dataset for federated learning
np.savez(dataset_npz_path, train_images=X, train_labels=y)
print("✅ Dataset saved to NPZ")

# === 🧠 Train + Upload + Evaluate using CiferClient ===
client = CiferClient(
    encoded_project_id="dk5uRGVZVTRmcnNsM290cGx0SFBIdz09",
    encoded_company_id="T3cxZW9RV0I1UGp6WEROR3dVby9VQT09",
    encoded_client_id="RU5pTGRlc0c1SFozVTBQTHVtZGdVdz09",
    base_api="http://localhost/PHPCIMANIA08_ppml/cifer-ppml1.1/FederatedApi",
    dataset_path=dataset_npz_path,
    model_path=model_path,
    use_encryption=False,
    epochs=5
)

client.run()
