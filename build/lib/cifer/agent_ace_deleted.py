from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import webbrowser
import nbformat
from nbclient import NotebookClient

app = Flask(__name__)
CORS(app)

CIFER_KERNEL_NAME = "cifer-kernel"          # internal Jupyter kernel name
CIFER_DISPLAY_NAME = "🧠 Cifer Kernel"   # display name in Jupyter

def get_jupyter_root_dir():
    try:
        from notebook import notebookapp
        servers = list(notebookapp.list_running_servers())
        if servers:
            return servers[0]['notebook_dir']
    except:
        pass
    return os.path.expanduser("~")

@app.route('/run_notebook', methods=['POST'])
def run_notebook():
    data = request.get_json()
    url = data.get("url")
    filename = os.path.basename(url)
    jupyter_root = get_jupyter_root_dir()
    save_path = os.path.join(jupyter_root, filename)
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        r = requests.get(url)
        with open(save_path, 'wb') as f:
            f.write(r.content)
        webbrowser.open(f"http://localhost:8888/notebooks/{filename}")
        nb = nbformat.read(open(save_path), as_version=4)
        client = NotebookClient(nb, kernel_name=CIFER_KERNEL_NAME)
        client.execute()
        return jsonify({"status": "success", "file": filename})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def run_agent_ace(port=9999):
    print(f"🚀 Starting agent-ace Flask server at http://localhost:{port}")
    print(f"⚙️  Using kernel: {CIFER_DISPLAY_NAME} ({CIFER_KERNEL_NAME})")
    app.run(port=port)
