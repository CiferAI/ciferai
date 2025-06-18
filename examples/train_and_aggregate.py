import os
import time
import requests
import numpy as np
from cifer import CiferClient
from tensorflow.keras.models import load_model

# ⚙️ Configuration
project_id = "dk5uRGVZVTRmcnNsM290cGx0SFBIdz09"
company_id = "T3cxZW9RV0I1UGp6WEROR3dVby9VQT09"
client_id = "RU5pTGRlc0c1SFozVTBQTHVtZGdVdz09"
dataset_path = "./datasets/Cifer-Fraud-Detection-Dataset-AF.npz"
model_path = "./trained_model/owner_model.h5"
base_api = "http://localhost/PHPCIMANIA08_ppml/cifer-ppml1.1/FederatedApi"

# 🧠 STEP 1: Train owner's model
print("📍 STEP 1: Training owner's model...")
client = CiferClient(
    encoded_project_id=project_id,
    encoded_company_id=company_id,
    encoded_client_id=client_id,
    base_api=base_api,
    dataset_path=dataset_path,
    model_path=model_path,
    use_encryption=False,
    epochs=3,
)
client.model = client.create_new_model_by_dataset()
trained_model, train_acc = client.train_model()
if trained_model:
    client.model.save(model_path)
    print(f"✅ Owner model trained with accuracy: {train_acc:.4f}")
else:
    print("❌ Owner training failed.")

# 📤 STEP 2: Upload owner's model
print("📤 STEP 2: Uploading owner's model to server...")
client.send_model_to_server()

# 📥 STEP 3: Aggregate models
print("📥 STEP 3: Aggregating client models...")
client.aggregate_from_api()

# 🧪 STEP 4: Evaluate aggregated model
print("🧪 STEP 4: Evaluating aggregated model...")
X, y = client.load_dataset()
if client.model and X is not None:
    loss, accuracy = client.model.evaluate(X, y, verbose=0)
    print(f"🎯 Aggregated Model Accuracy: {accuracy:.4f}, Loss: {loss:.4f}")
else:
    print("⚠️ Evaluation failed due to missing model or dataset.")

# 📤 STEP 5: Upload final aggregated model
print("📤 STEP 5: Uploading final aggregated model...")
agg_model_path = f"./trained_model/aggregated_{project_id}_{int(time.time())}.h5"
client.model.save(agg_model_path)

if os.path.exists(agg_model_path):
    with open(agg_model_path, 'rb') as f:
        files = {'model_file': f}
        payload = {
            'project_id': project_id,
            'company_id': company_id,
            'client_id': client_id,
            'accuracy': accuracy,
        }
        upload_url = f"{base_api}/save_aggregated_model"
        response = requests.post(upload_url, data=payload, files=files)
        print("✅ Upload Aggregated Response:", response.text)
else:
    print(f"❌ Aggregated model file not found: {agg_model_path}")
