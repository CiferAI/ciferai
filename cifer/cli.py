import argparse
import os
import sys
import subprocess
import requests
from cifer.agent_ace import run_agent_ace

def ensure_kernel_registered():
    kernel_name = "cifer-kernel"
    display_name = "🧠 Cifer Kernel"
    kernel_dir = os.path.expanduser(f"~/.local/share/jupyter/kernels/{kernel_name}")

    if os.path.exists(kernel_dir):
        return  # Already registered

    print(f"🚀 Registering Jupyter kernel: {display_name}")
    try:
        subprocess.run([
            sys.executable, "-m", "ipykernel", "install",
            "--user", "--name", kernel_name,
            "--display-name", display_name
        ], check=True)
        print(f"✅ Kernel registered as: {display_name}")
    except Exception as e:
        print(f"❌ Failed to register kernel: {e}")

def download_notebook(url):
    filename = url.split("/")[-1]
    try:
        r = requests.get(url)
        if r.status_code == 200:
            with open(filename, "wb") as f:
                f.write(r.content)
            print(f"✅ Notebook downloaded: {filename}")
        else:
            print(f"❌ Failed to download notebook. Status: {r.status_code}")
    except Exception as e:
        print(f"❌ Error downloading notebook: {e}")

def sync_folder(folder):
    print(f"🔁 Simulating sync of folder '{folder}' to remote server...")

def simulate_training(epochs, lr):
    print(f"🧪 Simulating training... Epochs: {epochs}, Learning Rate: {lr}")
    for i in range(1, epochs + 1):
        print(f"➡️  Epoch {i}/{epochs}... (lr={lr})")
    print("✅ Training simulation completed.")

def main():
    ensure_kernel_registered()

    parser = argparse.ArgumentParser(prog="cifer", description="Cifer CLI")
    subparsers = parser.add_subparsers(dest="command")

    # agent-ace
    agent_ace_parser = subparsers.add_parser("agent-ace", help="Run Flask server to download & execute Jupyter Notebook")
    agent_ace_parser.add_argument("--port", type=int, default=9999, help="Port to run the server on")

    # register-kernel
    subparsers.add_parser("register-kernel", help="Register ipykernel manually (optional)")

    # download-notebook
    notebook_parser = subparsers.add_parser("download-notebook", help="Download a Jupyter notebook from URL")
    notebook_parser.add_argument("--url", required=True, help="URL of the notebook")

    # sync
    sync_parser = subparsers.add_parser("sync", help="Simulate syncing folder to remote")
    sync_parser.add_argument("--folder", required=True, help="Folder to sync")

    # train
    train_parser = subparsers.add_parser("train", help="Simulate model training")
    train_parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs")
    train_parser.add_argument("--lr", type=float, default=0.001, help="Learning rate")

    args = parser.parse_args()

    if args.command == "agent-ace":
        run_agent_ace(port=args.port)
    elif args.command == "register-kernel":
        ensure_kernel_registered()
    elif args.command == "download-notebook":
        download_notebook(args.url)
    elif args.command == "sync":
        sync_folder(args.folder)
    elif args.command == "train":
        simulate_training(args.epochs, args.lr)
    else:
        parser.print_help()
