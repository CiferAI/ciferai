# ciferai.py

import flwr as fl
import numpy as np
import torch
from typing import Callable, Dict, Tuple
from flwr.common.logger import log

def get_eval_fn(model: torch.nn.Module, testloader: torch.utils.data.DataLoader) -> Callable[[], Tuple[float, float]]:
    """
    Returns an evaluation function for server-side evaluation.
    
    Args:
        model (torch.nn.Module): The PyTorch model to evaluate.
        testloader (torch.utils.data.DataLoader): The DataLoader for the test dataset.
    
    Returns:
        Callable: A function that returns a tuple (loss, accuracy) when called.
    """
    def evaluate() -> Tuple[float, float]:
        model.eval()
        loss, correct = 0, 0
        criterion = torch.nn.CrossEntropyLoss()
        with torch.no_grad():
            for data, target in testloader:
                output = model(data)
                loss += criterion(output, target).item() * data.size(0)
                pred = output.argmax(dim=1, keepdim=True)
                correct += pred.eq(target.view_as(pred)).sum().item()
        loss /= len(testloader.dataset)
        accuracy = correct / len(testloader.dataset)
        log("Evaluation complete: loss={:.4f}, accuracy={:.4f}".format(loss, accuracy))
        return loss, accuracy
    
    return evaluate

def set_initial_parameters(model: torch.nn.Module, init: np.ndarray):
    """
    Set initial parameters for the model from a NumPy array.
    
    Args:
        model (torch.nn.Module): The PyTorch model to update.
        init (np.ndarray): The initial parameters to set.
    """
    params = torch.tensor(init, dtype=torch.float32)
    with torch.no_grad():
        for param, init_param in zip(model.parameters(), params):
            param.copy_(init_param)
    log("Initial parameters set.")

def get_parameters(model: torch.nn.Module) -> np.ndarray:
    """
    Get the parameters of the model as a NumPy array.
    
    Args:
        model (torch.nn.Module): The PyTorch model to extract parameters from.
    
    Returns:
        np.ndarray: The model parameters as a NumPy array.
    """
    params = np.concatenate([param.detach().numpy().ravel() for param in model.parameters()])
    log("Parameters retrieved.")
    return params

def set_parameters(model: torch.nn.Module, params: np.ndarray):
    """
    Set the model parameters from a NumPy array.
    
    Args:
        model (torch.nn.Module): The PyTorch model to update.
        params (np.ndarray): The parameters to set.
    """
    params = torch.tensor(params, dtype=torch.float32)
    with torch.no_grad():
        for param, param_data in zip(model.parameters(), params):
            param.copy_(param_data.reshape(param.size()))
    log("Parameters updated.")

def create_cifer_client(model: torch.nn.Module, trainloader: torch.utils.data.DataLoader, testloader: torch.utils.data.DataLoader) -> fl.client.Client:
    """
    Create a Cifer client for Federated Learning.
    
    Args:
        model (torch.nn.Module): The PyTorch model used by the client.
        trainloader (torch.utils.data.DataLoader): The DataLoader for the training dataset.
        testloader (torch.utils.data.DataLoader): The DataLoader for the test dataset.
    
    Returns:
        fl.client.Client: A Cifer client that can participate in Federated Learning.
    """
    class CiferClient(fl.client.NumPyClient):
        def get_parameters(self) -> np.ndarray:
            log("Getting parameters.")
            return get_parameters(model)

        def set_parameters(self, parameters: np.ndarray):
            log("Setting parameters.")
            set_parameters(model, parameters)

        def fit(self, parameters: np.ndarray, config: Dict[str, int]) -> Tuple[np.ndarray, int, Dict]:
            log("Starting training.")
            set_parameters(model, parameters)
            model.train()
            optimizer = torch.optim.SGD(model.parameters(), lr=config["lr"])
            for data, target in trainloader:
                output = model(data)
                loss = torch.nn.functional.cross_entropy(output, target)
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            log("Training complete.")
            return get_parameters(model), len(trainloader.dataset), {}

        def evaluate(self, parameters: np.ndarray, config: Dict[str, int]) -> Tuple[float, int, Dict]:
            log("Starting evaluation.")
            set_parameters(model, parameters)
            loss, accuracy = get_eval_fn(model, testloader)()
            log("Evaluation complete.")
            return loss, len(testloader.dataset), {"accuracy": accuracy}
    
    return CiferClient()
