from cifer import CiferClient
from tensorflow.keras.models import load_model
import numpy as np

print("Initializing Cifer Client...")
client = CiferClient(
    encoded_project_id="dk5uRGVZVTRmcnNsM290cGx0SFBIdz09",
    encoded_company_id="T3cxZW9RV0I1UGp6WEROR3dVby9VQT09",
    encoded_client_id="RU5pTGRlc0c1SFozVTBQTHVtZGdVdz09",
    base_api="http://localhost/PHPCIMANIA08_ppml/cifer-ppml1.1//FederatedApi",
    dataset_path="./datasets/Cifer-Fraud-Detection-Dataset-AF.npz",
    model_path="./trained_model/fraud_model_agg.h5",
    use_encryption=False,
    epochs=1
)

print("Aggregating models from clients...")
client.aggregate_from_api()

# 🔁 Ensure model is loaded
if client.model is None:
    client.model = client.load_model()

print("Evaluating aggregated model...")
X_test, y_test = None, None
X, y = client.load_dataset()
if X is not None and y is not None:
    split = int(len(X) * 0.8)
    X_test, y_test = X[split:], y[split:]

if X_test is not None and y_test is not None:
    loss, accuracy = client.model.evaluate(X_test, y_test, verbose=0)
    print(f"Aggregated Model Accuracy: {accuracy:.4f}, Loss: {loss:.4f}")
else:
    print("Cannot evaluate model — dataset not loaded.")
