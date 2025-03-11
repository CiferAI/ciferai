import base64
import numpy as np
import tensorflow as tf
import os

def decode_id(encoded_id):
    return base64.b64decode(encoded_id).decode("utf-8")

def load_dataset(dataset_path=None):
    if dataset_path and os.path.exists(dataset_path):
        print(f"📂 Loading dataset from {dataset_path}...")
        return np.load(dataset_path)  # ✅ ต้องให้ dataset เป็น .npy หรือไฟล์ที่อ่านได้
    print("🔄 Loading MNIST dataset as default...")
    (train_images, train_labels), _ = tf.keras.datasets.mnist.load_data()
    return train_images / 255.0, train_labels

def save_model(model_data, model_path="model.h5"):
    with open(model_path, "wb") as f:
        f.write(model_data)
    return tf.keras.models.load_model(model_path)
