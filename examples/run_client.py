import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from datasets import load_dataset
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from cifer import CiferClient

dataset_hf_id = "CiferAI/Cifer-Fraud-Detection-Dataset-AF" 
dataset_csv_path = "./datasets/Cifer-Fraud-Detection-Dataset-AF.csv" 
dataset_npz_path = "./datasets/Cifer-Fraud-Detection-Dataset-AF.npz" 
model_path = "./trained_model/fraud_model.h5" 
dataset_path = ""

print("📥 Loading dataset ...") 
ds = load_dataset(dataset_hf_id) 
df = ds["train"].to_pandas() 
# ✅ Reduce the dataset size for faster training 
df = df.sample(n=100_000, random_state=42)
# 💾 Save CSV (optional)
os.makedirs(os.path.dirname(dataset_csv_path), exist_ok=True) 
df.to_csv(dataset_csv_path, index=False) 
print("✅ Dataset saved to CSV.") 
# === 🧼 CLEANING === 
df_clean = df.copy() 
df_clean = df_clean.apply(pd.to_numeric, errors='coerce').fillna(0) 
X = df_clean.iloc[:, :-1].astype(np.float32).to_numpy() 
y = df_clean.iloc[:, -1] 
if y.dtype == "object" or y.nunique() > 2: 
   y = LabelEncoder().fit_transform(y) 
else: 
   y = y.astype(np.int32) 
y = np.array(y).reshape(-1,) 
print(f"✅ Feature shape: {X.shape}, Label shape: {y.shape}") 
# === 🔁 SAVE DATASET AS NPZ FOR CIFER === 
np.savez(dataset_npz_path, train_images=X, train_labels=y) 
print("✅ Dataset saved to NPZ for CiferClient") 


# === 🚀 TRAIN MODEL === 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42) 
model = keras.Sequential([ 
    keras.layers.Input(shape=(X.shape[1],)),  
    keras.layers.Dense(64, activation="relu"),  
    keras.layers.Dense(32, activation="relu"),  
    keras.layers.Dense(1, activation="sigmoid")  
])  
model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"]) 
model.fit(X_train, y_train, epochs=1, batch_size=1024, verbose=1) 
# === 💾 SAVE MODEL === 
os.makedirs(os.path.dirname(model_path), exist_ok=True) 
model.save(model_path) 
print(f"✅ Model saved to {model_path}")


# === 🚀 RUN CIFER CLIENT === 
client = CiferClient( 
    encoded_project_id="VVR6LzRGVmJzeko4OUhGU1NGOHpoUT09", 
    encoded_company_id="WExRUmN2bjU2QVNISFJBRVFNNFllUT09", 
    encoded_client_id="WUNsVlRsUUoxWFF2d0ljRTVsWGl5QT09", 
    base_api="http://localhost/PHPCIMANIA08_ppml/cifer-ppml1.1//FederatedApi", 
    dataset_path=dataset_npz_path, 
    model_path=model_path, 
    use_encryption=False
)

client.run()