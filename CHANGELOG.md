# Changelog

## \[1.0.14] - 2025-05-30

### ✅ **\[New] Cifer CLI Agent & Kernel Integration**
* Added `cifer` CLI with subcommands:
  * `agent-ace` – Run Flask server to download & execute Jupyter Notebooks
  * `register-kernel` – Automatically register Jupyter kernel for current Conda environment
  * `download-notebook`, `sync`, and `train` – Utility commands for notebook management and testing
* Introduced auto-registration for **🧠 Cifer AI Kernel** (`cifer-kernel`) on all CLI usage
* Executed notebooks are now forced to run using the `cifer-kernel` for consistent environment behavior
* Flask agent `/run_notebook` endpoint downloads, executes, and opens notebooks inside Jupyter


## [1.0.13] - 2025-05-10

### ✅ **\[New] Homomorphic Encryption (HE) Support**

* Added `use_encryption=True` flag in both `CiferClient` and `CiferServer`
* Integrated `Paillier` encryption using the `phe` library to secure model weights
* Client now generates a keypair (`public_key`, `private_key`) and encrypts weights before upload
* Encrypted model weights are uploaded via the new `/upload_encrypted_model` API

---

### ✅ **\[New] Server-Side Encrypted Model Aggregation**

* Added `fetch_encrypted_models()` to retrieve encrypted weights from clients
* Implemented `encrypted_fed_avg()` to perform homomorphic FedAvg without decrypting
* Encrypted aggregation output is saved as `aggregated_encrypted_weights.pkl` for client-side decryption

---

### ✅ **\[New] PHP/CodeIgniter API Enhancements**

* Added new API endpoint: `get_encrypted_client_models($project_id)` to fetch encrypted models only
* Validates and stores encrypted models in the `model_updates` table
* Automatically updates the project status to "Testing in Progress" when a model is uploaded

---

### ✅ **\[Fixes] Server Run Script Improvements**

* Automatically creates `model_path` and `dataset_path` if not present
* Added `USE_ENCRYPTION` flag in the run script to easily toggle encryption mode

---

### ⚙️ **Dependencies**

* `phe>=1.5.0` for Paillier homomorphic encryption
* `tensorflow>=2.0`, `numpy>=1.19`

## [1.0.8] - 2025-04-11
### Added
- ✨ Integrated `flask-cors` to support browser-based communication with the local Agent
- 🌐 Added support for launching Jupyter notebooks via either `localhost` or a remote `open_url`
- 📦 Included JavaScript client snippet for calling the agent directly from a web page
- 🧪 Added support for Homomorphic Encryption workflows in the agent-client pipeline

### Improved
- 🧠 Refactored agent logic to dynamically handle notebook URLs and browser launch targets
- 🔐 Enhanced agent's compatibility with encrypted notebook execution scenarios using homomorphic encryption
- 📁 Improved compatibility with both local Jupyter and server-proxied environments (e.g., `/notebook` on `workspace.cifer.ai`)

### Fixed
- ✅ Corrected hardcoded browser path (`/notebooks/notebooks/filename`) to proper rendering path



## [1.0.6] - 2025-03-23
### Fixed
- 🛠️ Resolved bug in data processing related to incorrect input handling.
- ✅ Improved error handling for missing or corrupted dataset files.
- ⚡ Optimized model loading process to prevent `AttributeError` in `CiferClient`.
- 🔐 Fixed issue where encrypted parameters were not being properly decrypted:

## [1.0.4] - 2025-03-17
### Fixed
- 🛠️ Resolved bug in data processing related to incorrect input handling.
- ✅ Improved error handling for missing or corrupted dataset files.
- ⚡ Optimized model loading process to prevent `AttributeError` in `CiferClient`.

## [1.0.3] - 2025-03-11
### Fixed
- Resolved bug in data processing related to incorrect input handling.
- Added WebSocket connectivity improvements to enhance stability and performance.


## [1.0.2] - 2025-03-09
### Fixed
- Resolved bug in data processing related to incorrect input handling.

## [1.0.1] - 2025-03-07
### Added
- Initial release of `cifer`
- Implements Homomorphic Encryption (LightPHE)
- API Server integration with Flask and Uvicorn

## [0.1.26] - 2024-10-28
### Added
- Websocket server-client 
- PyJWT
### Fixed
- Resolved bug in data processing related to incorrect input handling.

## [0.1.26] - 2024-10-28
### Added
- Added support for WebSocket Secure (WSS), allowing users to choose between standard WebSocket (WS) or secure WSS communication.
- Enabled model weight encryption using Homomorphic Encryption (RSA) for secure data transmission between Client and Server. This can be enabled with the use_homomorphic parameter.
- Added JSON Web Token (JWT) authentication, requiring Clients to send a token to the Server for identity verification, enhancing access control.
### Fixed
- Resolved import issues by switching to absolute imports in connection_handler.py to reduce cross-package import conflicts when running the project externally.

## [0.1.23] - 2024-10-22
### Fixed
- Resolved bug in data processing related to incorrect input handling.

## [0.1.22] - 2024-10-05
### Fixed
- No matching distribution found for tensorflow
- Package versions have conflicting dependencies.

## [0.1.19] - 2024-09-29
### Added
- Add conditional TensorFlow installation based on platform
### Fixed
- Resolved bug in data processing related to incorrect input handling.

## [0.1.18] - 2024-09-29
### Added
- Initial release of `FedServer` class that supports federated learning using gRPC.
- Added client registration functionality with `clientRegister`.
- Added model training round management with `startServer` function.
- Implemented federated averaging (FedAvg) aggregation for model weights.
- Model validation functionality with `__callModelValidation` method.
- Support for handling multiple clients concurrently with threading.
- Configurable server via `config.json`.

### Changed
- Modularized the code for future extension and improvement.
- Created configuration options for server IP, port, and `max_receive_message_length` via the `config.json` file.

### Fixed
- Optimized client handling to prevent blocking during registration and learning rounds.


## [0.1.15-0.1.17] - 2024-09-14
### Fixed
- Resolved bug in data processing related to incorrect input handling.

## [0.1.14] - 2024-09-013
### Fixed
- Resolved bug in data processing related to incorrect input handling.

## [0.1.13] - 2024-09-08
### Added
-- Integrate Tensorflow and Huggingface's Transformer
New Integration: Added support for TensorFlow and HuggingFace's Transformers library to enhance model training and expand compatibility with popular AI frameworks.
### Fixed
-- Resolved various bugs to improve system stability and performance.
This update continues to build on CiferAI's federated learning and fully homomorphic encryption (FHE) framework, focusing on enhanced compatibility, privacy, and security in decentralized machine learning environments.

## [0.1.11] - 2024-09-08
### Changed
- Homepage --- cifer.ai
Documentation. --- cifer.ai/documentation
Repository --- https://github.com/CiferAI/ciferai

## [0.1.10] - 2024-09-08
### Changed
- Updated `README.md` to improve content and information about Cifer.

## [0.0.9] - 2024-09-01
### Added
- Added new feature for handling exceptions in the main module.
- Included additional error logging functionality.

## [0.0.8] - 2024-08-25
### Fixed
- Resolved bug in data processing related to incorrect input handling.