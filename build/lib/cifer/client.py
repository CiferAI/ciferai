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

        # ✅ โหลดโมเดล
        self.model = self.load_model()

    def load_dataset(self):
        """
        โหลด dataset จากไฟล์ หรือดึงจาก API
        """
        if os.path.exists(self.dataset_path):
            print(f"📂 Loading dataset from {self.dataset_path} ...")
            data = np.load(self.dataset_path)
            return data["train_images"], data["train_labels"]
        else:
            print("❌ Dataset not found! Please check dataset path.")
            return None, None

    def load_model(self):
        """
        โหลดโมเดลจากไฟล์หรือดึงจากเซิร์ฟเวอร์
        """
        if os.path.exists(self.model_path):
            print(f"📂 Loading model from {self.model_path} ...")
            return tf.keras.models.load_model(self.model_path)
        else:
            print("❌ Model file not found, attempting to download...")
            return self.download_model()

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
                print("❌ No valid model received. Creating new model...")
                return self.create_new_model()
        except Exception as e:
            print(f"❌ ERROR: {e}")
            return self.create_new_model()

    def create_new_model(self):
        """
        สร้างโมเดลใหม่หากไม่มีโมเดลให้โหลด
        """
        print("🛠️ Creating new model...")
        model = tf.keras.Sequential([
            tf.keras.layers.Flatten(input_shape=(28, 28)),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(10, activation="softmax")
        ])
        model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        model.save(self.model_path)
        print(f"✅ New model created and saved at {self.model_path}")
        return model

    def train_model(self):
        print("🚀 Training model...")

        # ✅ โหลด dataset
        train_images, train_labels = self.load_dataset()
        
        if train_images is None or train_labels is None:
            print("❌ ERROR: Dataset is empty or corrupted!")
            return None, None

        # ✅ ตรวจสอบว่าโมเดลถูกโหลดแล้วหรือไม่
        if self.model is None:
            print("❌ ERROR: Model not loaded! Cannot train.")
            return None, None

        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        history = self.model.fit(train_images, train_labels, epochs=1, batch_size=32, verbose=1)

        accuracy = history.history.get("accuracy", [None])[-1]
        if accuracy is None:
            print("❌ ERROR: Accuracy not found in training history!")
            return None, None

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
            "company_id": self.config.company_id,
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
