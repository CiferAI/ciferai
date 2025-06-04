<p align="left">
  <a href="https://cifer.ai/">
    <img src="https://cifer.ai/assets/themes/cifer/images/logo/ciferlogo.png" width="240" alt="Cifer Website" />
  </a>
</p>

Cifer is a **Privacy-Preserving Machine Learning (PPML) framework** offers several methods for secure, private, collaborative machine learning **“Federated Learning”** and **“Fully Homomorphic Encryption”**

[![GitHub license](https://img.shields.io/github/license/CiferAI/ciferai)](https://github.com/CiferAI/ciferai/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/CiferAI/ciferai/blob/main/CONTRIBUTING.md)
[![Downloads](https://static.pepy.tech/badge/cifer)](https://pepy.tech/project/cifer)

[🌎 Website](https://cifer.ai) &nbsp;&nbsp;| &nbsp;
[📔 Docs](https://cifer.ai/documentation) &nbsp;&nbsp;| &nbsp;
[🙌 Join Slack](https://join.slack.com/t/cifertalk/shared_invite/zt-2y09cb0yu-zHYyNkiYWq6AfssvU2rLrA)

<br>

## Table of content
1. <a href="#introduction">Introduction</a>
2. <a href="#installation">Installation</a>
3. <a href="#basic-usage-examples">Basic Usage Examples</a><br>
3.1 <a href="#basic-usage-examples-fedlearn">FedLearn</a><br>
3.2 <a href="#basic-usage-examples-fhe">FHE</a>

<br>

# Introduction

Cifer is a Privacy-Preserving Machine Learning (PPML) framework designed to revolutionize the way organizations approach secure, private, and collaborative machine learning. In an era where data privacy and security are paramount, Cifer offers a comprehensive solution that combines advanced technologies to enable privacy-conscious AI development and deployment.

## Core Modules
1. **Federated Learning (FedLearn):** Cifer's FedLearn module allows for decentralized machine learning, enabling multiple parties to collaborate on model training without sharing raw data.
2. **Fully Homomorphic Encryption (HomoCryption):** Our FHE framework permits computations on encrypted data, ensuring end-to-end privacy throughout the machine learning process.

## Key Features

1. **Flexible Architecture:** Cifer adapts to your needs, supporting both decentralized and centralized federated learning configurations.

2. **Enhanced Security and Privacy:** Leveraging advanced cryptographic techniques and secure communication protocols, Cifer provides robust protection against various privacy and security threats.

3. **Broad Integration:** Seamlessly integrates with popular machine learning tools and frameworks, including PyTorch, TensorFlow, scikit-learn, NumPy, JAX, Cuda, Hugging Face's Transformer; ensuring easy adoption across different environments.

4. **No-Code Configuration:** Simplify your setup with our intuitive no-code platform, making privacy-preserving machine learning accessible to a wider audience.

## Why Cifer Stands Out
Cifer offers a revolutionary approach to **Privacy-Preserving Machine Learning (PPML)** by combining powerful federated learning capabilities with robust encryption, ensuring privacy, security, and flexibility. Here are the key reasons why Cifer sets itself apart from other federated learning frameworks:

### 1. Customized Network Design: Decentralized (dFL) and Centralized (cFL) Options
Cifer’s FedLearn framework provides the flexibility to choose between Decentralized Federated Learning (dFL) and Centralized Federated Learning (cFL):

- **Decentralized Federated Learning (dFL):** Powered by Cifer’s proprietary blockchain and Layer-1 infrastructure, dFL ensures a robust, resilient system through its Byzantine Robust Consensus algorithm, even if some nodes are compromised or malicious. This fully decentralized approach is ideal for distributed environments where privacy and data ownership are paramount.

- **Centralized Federated Learning (cFL):** For organizations that prefer more control, such as trusted collaborations among known partners, cFL offers a centralized model that provides oversight and management flexibility. This centralized option is tailored for environments that require higher levels of governance.

### 2. Enhanced Security and Efficient Communication Protocol
Most federated learning frameworks on the market rely on Peer-to-Peer (P2P) protocols, which are vulnerable to security threats like man-in-the-middle attacks, data interception, and inefficiencies in communication.

Cifer uses the gRPC communication protocol, which leverages HTTP/2 for multiplexing, bidirectional streaming, and header compression, resulting in faster, more secure communication. By utilizing Protocol Buffers for serialization, Cifer ensures smaller message sizes, faster processing, and enhanced reliability. The built-in encryption and secure communication channels protect data exchanges from unauthorized access and tampering, making Cifer a more secure and efficient solution compared to P2P-based frameworks.

### 3. No-Code Configuration Platform
Cifer simplifies the complexity of setting up federated learning with its no-code configuration platform. Unlike other frameworks that require manual coding and intricate setups, Cifer provides an intuitive browser-based user interface that allows users to design, configure, and deploy federated learning systems without writing any code. This innovative approach lowers the barrier for organizations to adopt federated learning while ensuring flexibility and scalability.

### 4. FedLearn Combined with Fully Homomorphic Encryption (FHE)
Cifer uniquely combines FedLearn with Fully Homomorphic Encryption (FHE), enabling computations on encrypted data throughout the entire training process. This means that sensitive data never needs to be decrypted, providing end-to-end encryption for complete privacy. With the integration of FHE, organizations can train machine learning models on sensitive data without ever exposing it, ensuring that privacy and compliance standards are met, even when working in a collaborative environment.

<br><br>

# Installation

Pip The preferred way to install Cifer is through PyPI:
```
pip install cifer
```

<br>

To upgrade Cifer to the latest version, use:
```
pip install --upgrade cifer
```

> ### Note:
> - **For macOS:** You can run these commands in the Terminal application.
> - **For Windows:** Use Command Prompt or PowerShell.
> - **For Linux:** Use your preferred terminal emulator.
> - **For Google Colab:** Run these commands in a code cell, prefixed with an exclamation mark (e.g., !pip install cifer).
> - **For Jupyter Notebook:** You can use either a code cell with an exclamation mark or the %pip magic command (e.g., %pip install cifer).
> <br><br>

<br>

## Docker
You can get the Cifer docker image by pulling the latest version:
```
docker pull ciferai/cifer:latest
```
<br>

To use a specific version of Cifer, replace latest with the desired version number, for example:
```
docker pull ciferai/cifer:v1.0.0
```

<br><br>

# What's Included in pip install cifer
When you install Cifer using pip, you get access to the following components and features:

### Core Modules
- **FedLearn:** Our federated learning implementation, allowing for collaborative model training while keeping data decentralized.
- **HomoCryption:** Fully Homomorphic Encryption module for performing computations on encrypted data.

### Integrations
Cifer seamlessly integrates with popular machine learning frameworks:
TensorFlow, Pytorch, scikit-learn, Numpy, Cuda, JAX, Hugging Face’s Transformer 

### Utilities
-	Data preprocessing tools
-	Privacy-preserving metrics calculation
-	Secure aggregation algorithms

### Cryptographic Libraries
-	Integration with state-of-the-art homomorphic encryption libraries

### Communication Layer
-	gRPC-based secure communication protocols for federated learning

### Example Notebooks
-	Jupyter notebooks demonstrating Cifer's capabilities in various scenarios

### Command-line Interface (CLI)
- A user-friendly CLI for managing Cifer experiments and configurations

## Optional Dependencies
Some features may require additional dependencies. You can install them using:

```
pip install cifer[extra]
```
Where extra can be:<br>
`viz`: For visualization tools<br>
`gpu`: For GPU acceleration support<br>
`all`: To install all optional dependencies

<br><br>

# Importing Cifer
After installing Cifer, you can import its modules in your Python scripts or interactive environments. The two main modules, FedLearn and FHE (Fully Homomorphic Encryption), can be imported as follows:

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
from cifer import fedlearn as fl
from cifer import homocryption as fhe
```

<br><br>

# Basic Usage Examples
Here are some quick examples to get you started:

### Communication Methods in Cifer FedLearn
Cifer FedLearn supports two communication methods for federated learning:

### Method A: RPC Web API via Cifer Workspace
In this approach, users create an ID via the Cifer Workspace, allowing direct interaction with the Cifer FedLearn server through an RPC-based Web API. This method simplifies deployment as users do not need to set up their own server.


### Method B: WebSocket Server (Self-Hosted)
In this approach, users set up their own federated learning server within their company infrastructure. This provides full control over data and security, allowing for on-premise deployment and customization.

Choose the method that best fits your use case and infrastructure requirements.

<br>

## Method A: Using RPC Web API via Cifer Workspace

### Key Adjustments: FedLearn
**FedLearn** in Cifer operates with two roles (as referred to in [Cifer Workspace](https://workspace.cifer.ai/)):

- 👑 **Server (Fed Master)**: Sets up the communication channel, specifies the model path, initializes the dataset, receives model updates, performs aggregation, and sends the new model back to clients. This process continues until all aggregation rounds are completed.
<br><br>
- 🧑‍💻 **Client (Contributor)**: Connects to the communication channel, follows the server’s model configuration, loads a local dataset, trains on local data, and sends model updates to the server. This process repeats until all aggregation rounds are finished.

<br>

## Server Side

### 1. Importing Cifer

To use the Cifer FedLearn, start by importing the required module:

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
from cifer import CiferServer
```

<br>

### 2. Server Configuration (Fed Master)

The server initializes the federated learning process by setting up the communication channel, specifying the model path, and defining the initial dataset:

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
server = CiferServer(
    encoded_project_id="YOUR_PROJECT_ID",
    encoded_company_id="YOUR_COMPANY_ID",
    encoded_client_id="YOUR_CLIENT_ID",
    base_api="http://localhost:5000",
    dataset_path="YOUR_DATASET_PATH",
    model_path="YOUR_MODEL_PATH"
)
```

<br>

### 2.1 Setup Communication Channel

The `encoded_project_id`, `encoded_company_id`, and `encoded_client_id` are obtained from the [Cifer Workspace](https://workspace.cifer.ai/). These IDs ensure proper collaboration and data integrity.

Replace your IDs in the following lines:

```python
encoded_project_id="YOUR_PROJECT_ID",
encoded_company_id="YOUR_COMPANY_ID",
encoded_client_id="YOUR_CLIENT_ID"
```

### 2.2 Define Dataset

Specify the local path of the dataset:

```python
dataset_path = "YOUR_DATASET_PATH"
```

### 2.3 Define Model

Specify the local path of the model:

```python
model_path = "YOUR_MODEL_PATH"
```

<br>

> <br>
> Alternatively, you can load models in different ways:
> <br><br>

<br>

<h3><img src="https://cdn.iconscout.com/icon/free/png-512/free-github-icon-download-in-svg-png-gif-file-formats--logo-minimal-icons-pack-files-folders-436555.png?f=webp&w=512" width="20" style="vertical-align:top;">&nbsp; Git Clone:</h3>

You can use the following CLI command to clone a model repository into your computer:

```bash
git clone <model_repo_url> <destination_folder>
```

For example:

```bash
git clone https://github.com/example/repo.git models_folder/
```

After cloning, specify the model path in your code:

```python
model_path = "<destination_folder>/YOUR_MODEL.h5"
```

<br>

<h3><img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.svg" width="20" alt="Hugging Face" style="vertical-align:middle;" /> Hugging Face Model:</h3>

You can use the following CLI command to download a pre-trained model from Hugging Face:

```bash
pip install transformers
```

Hugging Face's `transformers` library provides access to pre-trained machine learning models for various tasks. This enables you to use ready-made models without training from scratch.

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("bert-base-uncased")
model.save_pretrained("YOUR_MODEL_FOLDER")
```

After downloading, specify the model path in your code:

```python
model_path = "YOUR_MODEL_FOLDER"
```

<br>

### 3. Start Aggregation Process

Start the server to begin receiving and aggregating model updates:

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
server.run()
```

<br><br>


## Client side

### 1. Importing Cifer Client

The code begins by importing Cifer’s federated learning module:

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
import cifer
```

Then, import other necessary modules:

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
import numpy as np
import tensorflow as tf
from tensorflow import keras
from cifer import CiferClient
import os
```

<br>

### 2. Client Configuration (Contributor)

Each client follows the server’s setup and prepares its dataset and model. This ensures that all nodes contributing to the same project operate within the same communication channel, allowing seamless collaboration and aggregation of model updates.

### 2.1 Define Dataset

Put the local dataset path in `dataset_path`, and set up the dataset configuration based on your own requirements.

In this example, we use the MNIST dataset, normalize pixel values, and save it as a NumPy file.

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
dataset_path = "YOUR_DATASET_PATH"
if not os.path.exists(dataset_path):
    print("📂 Creating new dataset...")
    (train_images, train_labels), _ = keras.datasets.mnist.load_data()
    train_images = train_images / 255.0  # Normalize
    np.save(dataset_path, (train_images, train_labels))  # Save as a Tuple (train_images, train_labels)
    print("✅ Dataset created successfully!")
```

<br>

### 2.2 Define Model

Put the local model path in `model_path`, and set up the model configuration based on your own requirements.

In this example, we define a simple neural network model, set loss and optimization metrics, and save it as an H5 file.

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
model_path = "YOUR_MODEL_PATH"
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
```

<br>

> <br>
> Alternatively, you can load models in different ways:
> <br><br>

<br>

<h3><img src="https://cdn.iconscout.com/icon/free/png-512/free-github-icon-download-in-svg-png-gif-file-formats--logo-minimal-icons-pack-files-folders-436555.png?f=webp&w=512" width="20" style="vertical-align:top;">&nbsp; Git Clone:</h3>

You can use the following CLI command to clone a model repository into your computer:

```bash
git clone <model_repo_url> <destination_folder>
```

For example:

```bash
git clone https://github.com/example/repo.git models_folder/
```

After cloning, specify the model path in your code:

```python
model_path = "<destination_folder>/YOUR_MODEL.h5"
```

<br>

<h3><img src="https://huggingface.co/datasets/huggingface/brand-assets/resolve/main/hf-logo.svg" width="20" alt="Hugging Face" style="vertical-align:middle;" /> Hugging Face Model:</h3>

You can use the following CLI command to download a pre-trained model from Hugging Face:

```bash
pip install transformers
```

Hugging Face's `transformers` library provides access to pre-trained machine learning models for various tasks. This enables you to use ready-made models without training from scratch.

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("bert-base-uncased")
model.save_pretrained("YOUR_MODEL_FOLDER")
```

After downloading, specify the model path in your code:

```python
model_path = "YOUR_MODEL_FOLDER"
```

<br>

### 2.3 Setup Communication Channel

The client must use the same communication settings as the server:

The `encoded_project_id`, `encoded_company_id`, and `encoded_client_id` can be obtained from the [Cifer Workspace](https://workspace.cifer.ai/). These IDs ensure that all contributors stay connected within the same communication channel for seamless collaboration.

In Cifer Workspace, the client is referred to as **'Contributor'** and follows the same communication, model, and training configuration as the server **('Fed Master').**

Replace only the ID values in the following section:

<div style="background:#353a42; width:fit-content; padding:6px 12px; border-radius:6px 6px 0 0; font-size:12px; font-family:monospace;">
<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="14" style="position:relative; top:2px; left:-1px;" alt="Python" /> Python</div>

```python
client = CiferClient(
    encoded_project_id="YOUR_PROJECT_ID",
    encoded_company_id="YOUR_COMPANY_ID",
    encoded_client_id="YOUR_CLIENT_ID",
    base_api="http://localhost:5000",
    dataset_path=dataset_path,
    model_path=model_path
)
```

<br>

### 3. Start Training Process

Begin training and send model updates to the server:

```python
client.run()
```

<br><br>

## Method B: Using a Self-Hosted WebSocket Server

### Setting Up a Federated Learning Server

This method allows users to set up their own federated learning server within their company infrastructure.

#### 1. Importing Cifer:
The code begins by importing Cifer’s federated learning module: `from cifer import fedlearn as fl`, which allows you to use the FedLearn framework in your federated learning setup.


#### 2. Defining Datasets:
The dataset is stored locally, and the path to the dataset is defined using `local_data_path`. Ensure your dataset is prepared and accessible in the specified directory on your local machine. This local path will be used to load data for federated learning:
```
local_data_path = "/path/to/local/data"
```

#### 3. Defining Models:
You can integrate models into Cifer’s FedLearn in three different ways, depending on your requirements:

<br>

**3.1 Local Model:**<br>
If you have a pre-trained model stored locally, you can specify the local path to the model and use it for training:
```
local_model_path = "/path/to/local/model"
```
<br>

**3.2 Git Clone:**<br>
If your model is hosted on GitHub, you can clone the repository directly into your environment using the `os.system("git clone ...")` command:
```
os.system("git clone https://github.com/your-repo/your-model-repo.git")
```
<br>

**3.3 Hugging Face Model:**<br>
You can integrate a pre-trained model from Hugging Face’s `transformers` library. For instance, you can load a BERT-based model like this:
```
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
```

### Code Example

```
# Import the necessary modules from the Cifer framework
from cifer import fedlearn as fl
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import os

# Define paths to local data and model
local_data_path = "/path/to/local/data"
local_model_path = "/path/to/local/model"

# Option to load a pre-trained Hugging Face model
model_name = "distilbert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Alternatively, clone a model repository from GitHub (if necessary)
os.system("git clone https://github.com/your-repo/your-model-repo.git")

# Initialize the federated learning server using Cifer's FedLearn
server = fl.Server()

# Define a federated learning strategy
strategy = fl.strategy.FedAvg(
    # Custom data and model paths for local storage and Hugging Face model usage
    data_path=local_data_path,
    model_path=local_model_path,
    model_fn=lambda: model,  # Hugging Face model used as the base model
)

# Start the federated learning process
if __name__ == "__main__":
    server.run(strategy)
```



<br><br>

## Basic Usage Examples: FHE

```
# Import Cifer's HomoCryption module for fully homomorphic encryption
from cifer import homocryption as hc

# Generate keys: Public Key, Private Key, and Relinearization Key (Relin Key)
public_key, private_key, relin_key = hc.generate_keys()

# Example data to be encrypted
data = [42, 123, 256]

# Encrypt the data using the Public Key
encrypted_data = [hc.encrypt(public_key, value) for value in data]

# Perform computations on encrypted data
# For example, adding encrypted values
encrypted_result = hc.add(encrypted_data[0], encrypted_data[1])

# Apply relinearization to reduce noise in the ciphertext
relinearized_result = hc.relinearize(encrypted_result, relin_key)

# Decrypt the result using the Private Key
decrypted_result = hc.decrypt(private_key, relinearized_result)

# Output the result
print("Decrypted result of encrypted addition:", decrypted_result)
```

<br>

### How It Works: FHE

#### Key Generation:
First, we generate the necessary keys for homomorphic encryption using `hc.generate_keys()`. This provides the Public Key (used for encrypting data), Private Key (for decrypting results), and Relinearization Key (used to reduce noise during operations on encrypted data).

#### Encrypting Data:
Data is encrypted using the Public Key with `hc.encrypt()`. In this example, a simple array of numbers is encrypted for further computations.

#### Performing Encrypted Computation:
Fully homomorphic encryption allows computations to be performed directly on encrypted data. Here, we add two encrypted values with `hc.add()` without decrypting them, maintaining privacy throughout the operation.

#### Relinearization:
Relinearization helps manage noise introduced by homomorphic operations, which is done with the Relin Key using `hc.relinearize()`.

#### Decryption:
After the computations are complete, the Private Key is used to decrypt the result with `hc.decrypt()`.

<br>

---
<br>

For more detailed information and access to the full documentation, please visit [www.cifer.ai](https://cifer.ai/docs)
