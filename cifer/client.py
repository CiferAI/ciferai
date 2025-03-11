import requests
import base64
import json
import tensorflow as tf
import numpy as np
import os
from cifer.config import CiferConfig  # ✅ ดึงค่า Config

class CiferClient:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id, base_api=None, dataset_path=None, model_path=None):
        """
        กำหนดค่าเริ่มต้นของ Client
        """
        self.config = CiferConfig(
            encoded_project_id, 
            encoded_company_id, 
            encoded_client_id, 
            base_api, 
            dataset_path, 
            model_path
        )
        self.api_url = self.config.base_api
        self.dataset_path = self.config.dataset_path
        self.model_path = self.config.model_path

    def load_dataset(self):
        """
        โหลด dataset จากไฟล์ หรือดึงจาก API
        """
        if os.path.exists(self.dataset_path):
            print(f"📂 Loading dataset from {self.dataset_path} ...")
            return np.load(self.dataset_path)
        else:
            print("❌ Dataset not found! Please check dataset path.")
            return None

    def download_model(self):
        """
        ดึงโมเดลล่าสุดจากเซิร์ฟเวอร์
        """
        url = f"{self.api_url}/get_latest_model/{self.config.project_id}"
        response = requests.get(url)

        try:
            data = response.json()
            if data.get("status") == "success":
                model_data = base64.b64decode(data["model"])
                with open(self.model_path, "wb") as f:
                    f.write(model_data)
                print(f"✅ Model downloaded successfully: {self.model_path}")
                return tf.keras.models.load_model(self.model_path)
            else:
                print("❌ No valid model received.")
                return None
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return None

    def train_model(self):
        print("🚀 Training model...")
        
        # ✅ ตรวจสอบว่า dataset มีอยู่จริง
        if not os.path.exists(self.dataset_path):
            print(f"❌ Dataset not found! Please check dataset path: {self.dataset_path}")
            return None  # ✅ ป้องกัน TypeError

        train_images, train_labels = np.load(self.dataset_path, allow_pickle=True)
        
        # ✅ ตรวจสอบค่า dataset ว่าโหลดถูกต้องไหม
        if train_images is None or train_labels is None:
            print("❌ ERROR: Dataset is empty or corrupted!")
            return None

        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        history = self.model.fit(train_images, train_labels, epochs=1, batch_size=32, verbose=1)
        
        accuracy = history.history.get("accuracy", [None])[-1]
        if accuracy is None:
            print("❌ ERROR: Accuracy not found in training history!")
            return None

        return self.model, accuracy  # ✅ คืนค่า model และ accuracy


    def upload_model(self, model, accuracy):
        """
        อัปโหลดโมเดลที่เทรนเสร็จแล้วกลับไปยังเซิร์ฟเวอร์
        """
        model.save(self.model_path)
        with open(self.model_path, "rb") as f:
            model_data = f.read()

        files = {"model_file": (self.model_path, model_data)}
        data = {
            "project_id": self.config.project_id,
            "client_id": self.config.client_id,
            "accuracy": accuracy
        }

        response = requests.post(f"{self.api_url}/upload_model", files=files, data=data)
        if response.status_code == 200:
            print("✅ Model uploaded successfully!")
        else:
            print("❌ Upload failed:", response.text)

    def run(self):
        print("🚀 Starting Federated Learning Cycle...")

        # ✅ ตรวจสอบ dataset ก่อนเริ่ม
        if not os.path.exists(self.dataset_path):
            print(f"❌ Dataset not found at {self.dataset_path}. Please check your dataset path.")
            return  # ✅ หยุดการทำงานถ้าไม่มี dataset

        model, accuracy = self.train_model()
        
        # ✅ ป้องกัน `TypeError: cannot unpack non-iterable NoneType`
        if model is None or accuracy is None:
            print("❌ ERROR: Training failed. Please check logs.")
            return

        print(f"✅ Training complete! Accuracy: {accuracy:.4f}")
        self.upload_model(model, accuracy)

