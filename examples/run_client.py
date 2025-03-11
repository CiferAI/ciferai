import numpy as np
import tensorflow as tf
from tensorflow import keras
from cifer import CiferClient
import os

# ✅ สร้าง Dataset ถ้ายังไม่มี
dataset_path = "./mnist.npy"
if not os.path.exists(dataset_path):
    print("📂 Creating new dataset...")
    (train_images, train_labels), _ = keras.datasets.mnist.load_data()
    train_images = train_images / 255.0  # Normalize
    np.save(dataset_path, (train_images, train_labels))  # ✅ บันทึกเป็น Tuple `(train_images, train_labels)`
    print("✅ Dataset created successfully!")

# ✅ สร้าง Model ถ้ายังไม่มี
model_path = "client_model.h5"
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

# ✅ รัน Client
client = CiferClient(
    encoded_project_id="SldOWlozQVNyR3FQa3FpYjhzL2U2Zz09",
    encoded_company_id="NHZvalZnOXlyTmRXaUZiZkc4QnJrUT09",
    encoded_client_id="S294ZE12eUNjbTZ6OHhHQjk2dnk4QT09",
    base_api="http://localhost:5000",
    dataset_path=dataset_path,
    model_path=model_path
)

client.run()
