import requests
import base64
import json
import tensorflow as tf
import numpy as np
import os
import pickle
import logging
try:
    from phe import paillier
    PHE_AVAILABLE = True
except ImportError:
    PHE_AVAILABLE = False

from cifer.config import CiferConfig

# Setup logging
logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(message)s')


class CiferClient:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id, base_api=None,
                 dataset_path=None, model_path=None, use_encryption=False, rounds=1, epochs=1):
        if isinstance(model_path, bool) and use_encryption is False:
            use_encryption = model_path
            model_path = None

        self.config = CiferConfig(
            encoded_project_id,
            encoded_company_id,
            encoded_client_id,
            base_api,
            dataset_path,
            model_path,
            use_encryption
        )

        self.api_url = self.config.base_api
        self.dataset_path = self.config.dataset_path
        self.model_path = self.config.model_path
        self.use_encryption = getattr(self.config, "use_encryption", False)
        self.rounds = rounds
        self.epochs = epochs

        if self.use_encryption:
            if not PHE_AVAILABLE:
                raise ImportError("⚠️ 'phe' library is required for encryption. Please install with: pip install phe")
            print("🔐 Homomorphic Encryption ENABLED")
            self.public_key, self.private_key = paillier.generate_paillier_keypair()
        else:
            print("🔓 Homomorphic Encryption DISABLED")

        self.model = self.load_model()

    def load_dataset(self):
        if os.path.exists(self.dataset_path):
            print(f"📂 Loading dataset from {self.dataset_path} ...")
            data = np.load(self.dataset_path)
            train_images, train_labels = data["train_images"], data["train_labels"]
            if train_images.ndim != 3 or train_images.shape[1:] != (28, 28):
                print("❌ Invalid dataset shape!")
                return None, None
            return train_images, train_labels
        else:
            print("❌ Dataset not found! Please check dataset path.")
            return None, None

    def load_model(self):
        if os.path.exists(self.model_path):
            print(f"📂 Loading model from {self.model_path} ...")
            return tf.keras.models.load_model(self.model_path)
        else:
            print("❌ Model file not found, attempting to download...")
            return self.download_model()

    def download_model(self):
        url = f"{self.api_url}/get_latest_model/{self.config.project_id}"
        try:
            response = requests.get(url, timeout=10)
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
            logging.error(f"Download failed: {e}")
            return self.create_new_model()

    def create_new_model(self):
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
        train_images, train_labels = self.load_dataset()
        if train_images is None or train_labels is None:
            print("❌ ERROR: Dataset is empty or corrupted!")
            return None, None

        if self.model is None:
            print("❌ ERROR: Model not loaded! Cannot train.")
            return None, None

        self.model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
        history = self.model.fit(train_images, train_labels, epochs=self.epochs, batch_size=32, verbose=1)

        accuracy = history.history.get("accuracy", [None])[-1]
        if accuracy is None:
            print("❌ ERROR: Accuracy not found in training history!")
            return None, None

        return self.model, accuracy

    def encrypt_weights(self, model):
        print("🔒 Encrypting model weights...")
        weights = model.get_weights()
        encrypted_weights = []
        for layer in weights:
            flat = layer.flatten()
            enc = [self.public_key.encrypt(float(x)) for x in flat]
            encrypted_weights.append(enc)
        shapes = [w.shape for w in weights]
        return encrypted_weights, shapes

    def upload_model(self, model, accuracy):
        try:
            if self.use_encryption:
                encrypted_weights, shapes = self.encrypt_weights(model)
                payload = {
                    "project_id": self.config.project_id,
                    "client_id": self.config.client_id,
                    "company_id": self.config.company_id,
                    "accuracy": accuracy,
                    "encrypted_weights": base64.b64encode(pickle.dumps(encrypted_weights)).decode(),
                    "weights_shape": base64.b64encode(pickle.dumps(shapes)).decode()
                }
                response = requests.post(f"{self.api_url}/upload_encrypted_model", json=payload, timeout=10)
            else:
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
                response = requests.post(f"{self.api_url}/upload_model", files=files, data=data, timeout=10)

            if response.status_code == 200:
                print("✅ Model uploaded successfully!")
                logging.info(f"Upload success. Accuracy: {accuracy}")
            else:
                print("❌ Upload failed:", response.text)
                logging.error(f"Upload failed: {response.text}")
        except Exception as e:
            logging.error(f"Upload error: {e}")
            print("❌ Upload Exception:", str(e))

    def run(self):
        print("🚀 Starting Federated Learning Cycle...")
        if not os.path.exists(self.dataset_path):
            print(f"❌ Dataset not found at {self.dataset_path}. Please check your dataset path.")
            return

        for round_num in range(1, self.rounds + 1):
            print(f"\n🔁 Round {round_num}/{self.rounds}")
            logging.info(f"Start Round {round_num}")

            model, accuracy = self.train_model()
            if model is None or accuracy is None:
                print("❌ ERROR: Training failed. Please check logs.")
                return

            print(f"✅ Training complete! Accuracy: {accuracy:.4f}")
            self.upload_model(model, accuracy)
