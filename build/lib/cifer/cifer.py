# cifer.py
import logging
from typing import List, Tuple, Callable, Any

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CiferClient:
    def __init__(self, cid: str):
        self.cid = cid
        logger.info(f"CiferClient {cid} initialized.")

    def fit(self, parameters: List[float], num_rounds: int) -> Tuple[List[float], int]:
        logger.info(f"Client {self.cid} is training with parameters {parameters} for {num_rounds} rounds.")
        # Implement training logic here
        # Return updated parameters and number of rounds completed
        updated_parameters = parameters  # Example: no real update
        return updated_parameters, num_rounds

    def evaluate(self, parameters: List[float]) -> float:
        logger.info(f"Client {self.cid} is evaluating with parameters {parameters}.")
        # Implement evaluation logic here
        # Return evaluation score
        score = 0.0  # Example: dummy score
        return score

class CiferServer:
    def __init__(self):
        self.clients = []
        logger.info("CiferServer initialized.")

    def register_client(self, client: CiferClient):
        self.clients.append(client)
        logger.info(f"Client {client.cid} registered.")

    def aggregate(self, client_parameters: List[List[float]]) -> List[float]:
        logger.info("Aggregating parameters from clients.")
        # Implement aggregation logic here
        # Example: simple averaging
        num_clients = len(client_parameters)
        aggregated_parameters = [sum(p[i] for p in client_parameters) / num_clients for i in range(len(client_parameters[0]))]
        return aggregated_parameters

    def start_round(self, num_rounds: int):
        logger.info(f"Starting training round with {num_rounds} rounds.")
        for client in self.clients:
            params = [0.0] * 10  # Example: initial parameters
            updated_params, _ = client.fit(params, num_rounds)
            logger.info(f"Client {client.cid} updated parameters.")
            # Example: store or use updated_params

        # Aggregate parameters from clients
        client_params = [client.fit([0.0] * 10, num_rounds)[0] for client in self.clients]
        aggregated_params = self.aggregate(client_params)
        logger.info("Training round completed.")

# Helper functions
def create_client(cid: str) -> CiferClient:
    return CiferClient(cid)

def create_server() -> CiferServer:
    return CiferServer()

if __name__ == "__main__":
    # Example usage
    server = create_server()
    client1 = create_client("client1")
    client2 = create_client("client2")
    
    server.register_client(client1)
    server.register_client(client2)
    
    server.start_round(num_rounds=5)
