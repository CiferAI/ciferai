class CiferConfig:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id, base_api=None, dataset_path="dataset.npy", model_path="model.h5"):
        """
        # Configure connection settings for CiferClient and CiferServer

        """
        self.project_id = encoded_project_id
        self.company_id = encoded_company_id
        self.client_id = encoded_client_id
        self.base_api = base_api or "https://workspace.cifer.ai/FederatedApi"
        self.dataset_path = dataset_path
        self.model_path = model_path
