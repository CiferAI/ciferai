from cifer.config import CiferConfig
import requests
import base64
import os
import tensorflow as tf
import numpy as np

class CiferServer:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id, base_api="http://localhost:5000", dataset_path=None, model_path=None):
        self.project_id = encoded_project_id
        self.company_id = encoded_company_id
        self.client_id = encoded_client_id
        self.base_api = base_api  
        self.dataset_path = dataset_path  
        self.model_path = model_path  # ✅ เพิ่ม model_path

        print(f"🚀 Server Initialized! Base API: {self.base_api}")
        if self.dataset_path:
            print(f"📂 Dataset Path: {self.dataset_path}")
        if self.model_path:
            print(f"📦 Using Local Model: {self.model_path}")

    def load_model(self):
        """
        ✅ โหลดโมเดลจากไฟล์ (ถ้ามี) หรือจาก Clients
        """
        if self.model_path and os.path.exists(self.model_path):
            print(f"✅ Loading Local Model: {self.model_path}")
            return tf.keras.models.load_model(self.model_path)

        print("🔄 No Local Model Found. Fetching from Clients...")
        return self.fetch_client_models()

    def fetch_client_models(self):
        """
        ✅ ดึงโมเดลจาก Clients ผ่าน API
        """
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

    def load_models(self, model_data_list):
        """
        ✅ แปลงโมเดลจาก Base64 และโหลดเป็น TensorFlow Model
        """
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
        """
        ✅ Aggregation แบบ FedAvg (ค่าเฉลี่ยของ weights)
        """
        print("🔄 Performing FedAvg Aggregation...")

        if not models:
            print("❌ ERROR: No models to aggregate.")
            return None

        weights = [model.get_weights() for model in models]
        avg_weights = [np.mean(w, axis=0) for w in zip(*weights)]
        models[0].set_weights(avg_weights)  

        return models[0]

    def upload_aggregated_model(self, model):
        """
        อัปโหลดโมเดล Aggregation ไปยังเซิร์ฟเวอร์
        """
        if not self.base_api:
            print("❌ ERROR: Base API URL is missing!")
            return

        filename = "aggregated_model.h5"
        model.save(filename)

        with open(filename, "rb") as f:
            model_data = f.read()

        files = {"aggregated_model": (filename, model_data)}
        data = {
            "project_id": self.project_id,
            "aggregation_method": "FedAvg"
        }

        api_url = f"{self.base_api}/upload_aggregated_model"
        print(f"📡 Uploading aggregated model to {api_url}...")  # ✅ Debugging จุดนี้

        response = requests.post(api_url, files=files, data=data)

        if response.status_code == 200:
            print("✅ Aggregated model uploaded successfully!")
        else:
            print(f"❌ Upload failed: {response.text}")


    def run(self):
        """
        ✅ กระบวนการ Aggregation
        """
        print("✅ Server is running...")

        model = self.load_model()
        if not model:
            print("❌ ERROR: No model available for aggregation.")
            return

        aggregated_model = self.fed_avg([model])
        if aggregated_model:
            self.upload_aggregated_model(aggregated_model)
