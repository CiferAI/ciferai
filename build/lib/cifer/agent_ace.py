from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests
import webbrowser
import nbformat
from nbclient import NotebookClient
import uvicorn

app = FastAPI()

# 🔓 Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧠 Configuration
CIFER_KERNEL_NAME = "cifer-kernel"
CIFER_DISPLAY_NAME = "🧠 Cifer Kernel"

# 📦 Pydantic model to receive data from client
class NotebookRequest(BaseModel):
    url: str

# 📂 Function to get Jupyter's root directory
def get_jupyter_root_dir():
    try:
        from notebook import notebookapp
        servers = list(notebookapp.list_running_servers())
        if servers:
            return servers[0]['notebook_dir']
    except:
        pass
    return os.path.expanduser("~")

# 🧪 API endpoint to run notebook
@app.post("/run_notebook")
async def run_notebook(data: NotebookRequest):
    url = data.url
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

        return {"status": "success", "file": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ▶️ Function to start the FastAPI server
def run_agent_ace(port: int = 9999):
    print(f"🚀 Starting agent-ace FastAPI server at http://localhost:{port}")
    print(f"⚙️  Using kernel: {CIFER_DISPLAY_NAME} ({CIFER_KERNEL_NAME})")
    uvicorn.run("your_script_name:app", host="0.0.0.0", port=port, reload=True)

# 🔁 NOTE: Replace `your_script_name` with the name of your Python file (without the .py extension)
