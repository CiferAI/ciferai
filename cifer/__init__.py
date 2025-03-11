from .config import CiferConfig
from .client import CiferClient
from .server import CiferServer
from .connection_handler import run_federated_server
from .training import train_custom_model
from importlib.metadata import version, PackageNotFoundError

__all__ = ["CiferClient", "CiferServer", "CiferConfig"]

try:
    __version__ = version("cifer")
except PackageNotFoundError:
    __version__ = "unknown"


