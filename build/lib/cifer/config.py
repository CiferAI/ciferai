class CiferConfig:
    def __init__(self, encoded_project_id, encoded_company_id, encoded_client_id, base_api=None, dataset_path="dataset.npy", model_path="model.h5"):
        """
        กำหนดค่าการเชื่อมต่อของ CiferClient และ CiferServer
        """
        self.project_id = encoded_project_id
        self.company_id = encoded_company_id
        self.client_id = encoded_client_id
        self.base_api = base_api or "http://localhost:5000"
        self.dataset_path = dataset_path
        self.model_path = model_path
