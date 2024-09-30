<p align="left">
  <a href="https://cifer.ai/">
    <img src="https://cifer.ai/assets/themes/cifer/images/logo/ciferlogo.png" width="240" alt="Cifer Website" />
  </a>
</p>

Cifer is a **Privacy-Preserving Machine Learning (PPML) framework** offers several methods for secure, private, collaborative machine learning **“Federated Learning”** and **“Fully Homomorphic Encryption”**

[![GitHub license](https://img.shields.io/github/license/CiferAI/ciferai)](https://github.com/CiferAI/ciferai/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/CiferAI/ciferai/blob/main/CONTRIBUTING.md)
[![Downloads](https://static.pepy.tech/badge/cifer)](https://pepy.tech/project/cifer)

[Website](https://cifer.ai) | 
[Docs](https://cifer.ai/documentation)

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

<img src="https://cifer.ai/assets/themes/cifer/images/icon/icon-python.png" width="16" alt="Python" /> &nbsp;Python

```
from cifer import fedlearn as fl
from cifer import homocryption as fhe
```

<br><br>

# Basic Usage Examples
Here are some quick examples to get you started:

## Basic Usage Examples: FedLearn
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

### Key Adjustments: FedLearn

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

<br>

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

## Example Dataset

In our example, we use the **[IQOTHNCCD Lung Cancer Dataset](https://www.kaggle.com/datasets/adityamahimkar/iqothnccd-lung-cancer-dataset?resource=download)** from Kaggle. This dataset is used to demonstrate Cifer’s machine learning capabilities in a healthcare context.

<br>

---

<br>

For more details, please visit the [Cifer Website](https://cifer.ai) for project information and the [Cifer Documentation](https://cifer.ai/documentation) for comprehensive documentation.
