import requests
import base64
import json
import tensorflow as tf
import numpy as np
import os
import tempfile
import logging
from tensorflow import keras
from tensorflow.keras.models import load_model

# Try importing Paillier encryption (partially homomorphic encryption)
try:
    from phe import paillier
    PHE_AVAILABLE = True
except ImportError:
    PHE_AVAILABLE = False

# Try importing PyTorch Geometric for Graph datasets
try:
    import torch
    import torch.nn.functional as F
    from torch_geometric.data import Data
    from torch_geometric.nn import GCNConv
    GRAPH_AVAILABLE = True
except ImportError:
    GRAPH_AVAILABLE = False

# HuggingFace support
try:
    from datasets import load_dataset as hf_load_dataset
    from transformers import AutoTokenizer, TFAutoModelForSequenceClassification
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

from cifer.config import CiferConfig

logging.basicConfig(filename='client.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class GCN(torch.nn.Module):
    def __init__(self, in_channels, hidden_channels, out_channels):
        super(GCN, self).__init__()
        self.conv1 = GCNConv(in_channels, hidden_channels)
        self.conv2 = GCNConv(hidden_channels, out_channels)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)

class CiferClient:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id, base_api=None, dataset_path=None, model_path=None, use_encryption=False, epochs=1):
        print("Initializing Cifer Client...")
        self.config = type('Config', (), {})()
        self.config.project_id = encoded_project_id
        self.config.company_id = encoded_company_id
        self.config.client_id = encoded_client_id
        self.config.base_api = base_api
        self.config.dataset_path = dataset_path
        self.config.model_path = model_path
        self.config.use_encryption = use_encryption
        self.config.epochs = epochs

        self.project_id = encoded_project_id
        self.company_id = encoded_company_id
        self.client_id = encoded_client_id
        self.base_api = base_api
        self.dataset_path = dataset_path
        self.model_path = model_path
        self.use_encryption = use_encryption
        self.epochs = epochs

        if self.use_encryption:
            if not PHE_AVAILABLE:
                raise ImportError("'phe' library is required for encryption. Install with: pip install phe")
            print("Homomorphic Encryption ENABLED")
            self.public_key, self.private_key = paillier.generate_paillier_keypair()
        else:
            print("Homomorphic Encryption DISABLED")

        self.dataset_type = "graph" if self.dataset_path.endswith(".pt") else "standard"
        if os.path.exists(self.dataset_path) and os.path.exists(self.model_path):
            self.model = self.load_model()
        else:
            self.model = None

        self.latest_accuracy = None

    def load_dataset(self):
        print("Loading dataset...")
        if self.dataset_type == "graph":
            if not GRAPH_AVAILABLE:
                raise ImportError("PyTorch Geometric not installed. Please install required packages.")
            return torch.load(self.dataset_path)

        if os.path.exists(self.dataset_path):
            try:
                data = np.load(self.dataset_path)
                train_images = data["train_images"]
                train_labels = data["train_labels"]
            except Exception as e:
                print(f"Error loading dataset: {e}")
                return None, None
            return train_images, train_labels
        else:
            print("Dataset not found!")
            return None, None

    def load_model(self):
        print("Loading or creating model...")
        if os.path.exists(self.model_path):
            if self.dataset_type == "graph":
                return None  # GCN model will be initialized in train_gnn_model
            return tf.keras.models.load_model(self.model_path)
        else:
            return self.create_new_model_by_dataset()

    def create_new_model_by_dataset(self):
        if self.dataset_type == "graph":
            print("Skipping model creation for graph dataset (GCN model will be created later).")
            return None

        train_images, train_labels = self.load_dataset()
        if train_images is None:
            raise ValueError("Dataset not found or invalid.")

        input_shape = train_images.shape[1:]
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=input_shape),
            tf.keras.layers.Flatten() if len(input_shape) > 1 else tf.keras.layers.Lambda(lambda x: x),
            tf.keras.layers.Dense(64, activation="relu"),
            tf.keras.layers.Dense(32, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid")
        ])
        model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        model.save(self.model_path)
        return model

    def train_model(self):
        if self.dataset_type == "graph":
            return self.train_gnn_model()

        train_images, train_labels = self.load_dataset()
        if train_images is None:
            return None, None

        if self.model is None:
            return None, None

        expected_shape = self.model.input_shape[1:]
        actual_shape = train_images.shape[1:]
        if expected_shape != actual_shape:
            print(f"Shape mismatch: expected {expected_shape}, got {actual_shape}")
            return None, None

        self.model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
        history = self.model.fit(train_images, train_labels, epochs=self.epochs, batch_size=32, verbose=1)
        accuracy = history.history.get("accuracy", [None])[-1]
        self.latest_accuracy = accuracy
        return self.model, accuracy

    def train_gnn_model(self):
        data = self.load_dataset()
        if not GRAPH_AVAILABLE:
            print("PyTorch Geometric not available.")
            return None, None

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        data = data.to(device)
        model = GCN(data.num_node_features, 16, int(data.y.max().item()) + 1).to(device)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

        model.train()
        for epoch in range(self.epochs):
            optimizer.zero_grad()
            out = model(data)
            loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
            loss.backward()
            optimizer.step()
            print(f"Epoch {epoch+1}/{self.epochs}, Loss: {loss.item():.4f}")

        model.eval()
        _, pred = model(data).max(dim=1)
        correct = pred[data.test_mask].eq(data.y[data.test_mask]).sum().item()
        acc = correct / int(data.test_mask.sum())
        self.latest_accuracy = acc
        torch.save(model.state_dict(), self.model_path.replace(".h5", ".pt"))
        return model, acc

    def fetch_models_from_api(self):
        url = f"{self.base_api}/get_model_list"
        try:
            response = requests.get(url, params={"project_id": self.project_id}, timeout=10)
            response.raise_for_status()
            model_json = response.json()
        except Exception as e:
            print(f"❌ Failed to fetch models from API: {e}")
            return []

        models = []
        for model_entry in model_json:
            model_url = model_entry.get("model_path")
            if not model_url:
                continue
            try:
                r = requests.get(model_url, timeout=15)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".h5") as tmp:
                    tmp.write(r.content)
                    tmp.flush()
                    model = load_model(tmp.name)
                    models.append(model.get_weights())
            except Exception as e:
                print(f"⚠️ Failed to load one model: {e}")
                continue
        return models
    

    def aggregate_from_api(self):
        weights_list = self.fetch_models_from_api()
        if len(weights_list) < 2:
            print("⚠️ Not enough models to aggregate")
            return
        print(f"📦 Aggregating {len(weights_list)} models via API...")
        self.aggregate_weights(weights_list)
        print("✅ Aggregated and updated local model")

    def aggregate_weights(self, weights_list):
        if not weights_list:
            print("❌ No weights to aggregate")
            return
        if isinstance(weights_list[0], list):
            avg_weights = [np.mean([w[i] for w in weights_list], axis=0) for i in range(len(weights_list[0]))]
            self.set_model_weights(avg_weights)

    def set_model_weights(self, weights):
        if self.model:
            self.model.set_weights(weights)

    def get_model_weights(self):
        if self.model:
            return self.model.get_weights()
        return None

    def run(self):
        print("Starting Federated Learning...")
        if not os.path.exists(self.dataset_path):
            print("Dataset not found.")
            return

        model, accuracy = self.train_model()
        if model is None or accuracy is None:
            print("Training failed.")
            return

        print(f"Training complete. Accuracy: {accuracy:.4f}")
        self.send_model_to_server()

    def send_model_to_server(self):
        if not self.base_api:
            print("No API endpoint configured")
            return
        print("📤 Uploading model file to server (multipart/form-data)...")

        model_file_path = self.model_path
        if self.dataset_type == "graph":
            model_file_path = self.model_path.replace(".h5", ".pt")

        if not os.path.exists(model_file_path):
            print(f"❌ Model file not found: {model_file_path}")
            return

        try:
            with open(model_file_path, "rb") as f:
                files = {
                    "model_file": (os.path.basename(model_file_path), f)
                }
                data = {
                    "project_id": self.project_id,
                    "company_id": self.company_id,
                    "client_id": self.client_id,
                    "accuracy": self.latest_accuracy
                }

                res = requests.post(f"{self.base_api}/send_model_to_server", data=data, files=files)
                res.raise_for_status()
                print(f"✅ Server response: {res.json()}")
        except Exception as e:
            print(f"❌ Upload failed: {e}")

