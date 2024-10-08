# Changelog

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