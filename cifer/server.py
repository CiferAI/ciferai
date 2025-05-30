import requests
import base64
import os
import tensorflow as tf
import numpy as np
import pickle

try:
    from phe import paillier
    PHE_AVAILABLE = True
except ImportError:
    PHE_AVAILABLE = False

class CiferServer:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id,
                 base_api="https://workspace.cifer.ai/FederatedApi", dataset_path=None,
                 model_path=None, use_encryption=False):
        self.project_id = encoded_project_id
        self.company_id = encoded_company_id
        self.client_id = encoded_client_id
        self.base_api = base_api
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.use_encryption = use_encryption
        print(f"🚀 Server Initialized! Encryption: {'ENABLED' if self.use_encryption else 'DISABLED'}")

        if self.use_encryption and not PHE_AVAILABLE:
            raise ImportError("Please install 'phe' for encrypted aggregation: pip install phe")
    def load_model(self):
        if self.model_path and os.path.exists(self.model_path):
            print(f"✅ Loading Local Model: {self.model_path}")
            return tf.keras.models.load_model(self.model_path)

        print("🔄 No Local Model Found. Fetching from Clients...")
        return self.fetch_client_models()
    def fetch_client_models(self):
        url = f"{self.base_api}/get_client_models/{self.project_id}"
        response = requests.get(url)

        try:
            data = response.json()
            if data.get("status") == "success":
                return self.load_models(data.get("models", []))
            else:
                print("❌ ERROR: No models found for aggregation.")
                return None
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return None

    def fetch_encrypted_models(self):
        url = f"{self.base_api}/get_client_models/{self.project_id}"
        response = requests.get(url)

        try:
            data = response.json()
            if data.get("status") == "success":
                models = []
                for m in data["models"]:
                    binary = base64.b64decode(m["model_data"])
                    encrypted_weights = pickle.loads(binary)
                    models.append(encrypted_weights)
                return models
            else:
                print("❌ ERROR: No encrypted models found.")
                return []
        except Exception as e:
            print(f"❌ ERROR loading encrypted models: {e}")
            return []

    def load_models(self, model_data_list):
        models = []
        for i, model_info in enumerate(model_data_list):
            try:
                model_data = base64.b64decode(model_info["model_data"])
                filename = f"client_model_{i}.h5"
                with open(filename, "wb") as f:
                    f.write(model_data)

                model = tf.keras.models.load_model(filename)
                models.append(model)
            except Exception as e:
                print(f"❌ ERROR: Failed to load model {i} - {e}")
        return models

    def fed_avg(self, models):
        print("🔄 Performing FedAvg Aggregation...")
        if not models:
            print("❌ ERROR: No models to aggregate.")
            return None

        weights = [model.get_weights() for model in models]
        avg_weights = [np.mean(w, axis=0) for w in zip(*weights)]
        models[0].set_weights(avg_weights)
        return models[0]

    def encrypted_fed_avg(self, encrypted_models):
        print("🔐 Performing Encrypted FedAvg Aggregation...")

        if not encrypted_models:
            print("❌ ERROR: No encrypted weights received.")
            return None

        # zip over each client's encrypted weight layers
        averaged = []
        for layers in zip(*encrypted_models):
            sum_layer = []
            for weights in zip(*layers):  # zip over each element in the layer
                summed = weights[0]
                for w in weights[1:]:
                    summed += w
                sum_layer.append(summed / len(encrypted_models))  # average
            averaged.append(sum_layer)

        print("✅ Encrypted aggregation complete (still encrypted)")
        return averaged  # still encrypted, must be decrypted by client who owns private key

    def upload_aggregated_model(self, model):
        filename = "aggregated_model.h5"
        model.save(filename)

        with open(filename, "rb") as f:
            model_data = f.read()

        files = {"aggregated_model": (filename, model_data)}
        data = {
            "project_id": self.project_id,
            "aggregation_method": "FedAvg",
            "num_clients": 1,
            "weight_statistics": '{"accuracy": null}'
        }

        api_url = f"{self.base_api}/upload_aggregated_model"
        print(f"📡 Uploading aggregated model to {api_url}...")
        response = requests.post(api_url, files=files, data=data)

        if response.status_code == 200:
            print("✅ Aggregated model uploaded successfully!")
        else:
            print(f"❌ Upload failed: {response.text}")

    def run(self):
        print("✅ Server is running...")

        if self.use_encryption:
            encrypted_models = self.fetch_encrypted_models()
            if not encrypted_models:
                print("❌ No encrypted models to aggregate.")
                return

            aggregated_weights = self.encrypted_fed_avg(encrypted_models)

            # ส่งต่อ encrypted weights ไปยัง client สำหรับการถอดรหัส
            filename = "aggregated_encrypted_weights.pkl"
            with open(filename, "wb") as f:
                pickle.dump(aggregated_weights, f)

            print(f"📦 Encrypted aggregated weights saved to {filename}")
            print("🛑 Waiting for client to decrypt and use aggregated model.")
            return

        models = self.load_model()
        if not models:
            print("❌ No model available for aggregation.")
            return

        aggregated_model = self.fed_avg([models]) if isinstance(models, list) else self.fed_avg([models])
        if aggregated_model:
            self.upload_aggregated_model(aggregated_model)
