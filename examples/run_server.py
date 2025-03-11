import numpy as np
import tensorflow as tf
from tensorflow import keras
from cifer import CiferServer
import os

# ✅ สร้าง Dataset ถ้ายังไม่มี
dataset_path = "./mnist.npy"
if not os.path.exists(dataset_path):
    print("📂 Creating new dataset...")
    (train_images, _), _ = keras.datasets.mnist.load_data()
    train_images = train_images / 255.0  # Normalize
    np.save(dataset_path, train_images)
    print("✅ Dataset created successfully!")

# ✅ สร้าง Model ถ้ายังไม่มี
model_path = "server_model.h5"
if not os.path.exists(model_path):
    print("🛠️ Creating new model...")
    model = keras.Sequential([
        keras.layers.Flatten(input_shape=(28, 28)),
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dense(10, activation="softmax")
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.save(model_path)
    print("✅ Model created and saved successfully!")

# ✅ รันเซิร์ฟเวอร์
server = CiferServer(
    encoded_project_id="SldOWlozQVNyR3FQa3FpYjhzL2U2Zz09",
    encoded_company_id="NHZvalZnOXlyTmRXaUZiZkc4QnJrUT09",
    encoded_client_id="S294ZE12eUNjbTZ6OHhHQjk2dnk4QT09",
    base_api="",
    dataset_path=dataset_path,
    model_path=model_path
)

server.run()
