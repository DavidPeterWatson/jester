from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

# Define the storage abstraction class
class StorageBackend:
    def load_config(self):
        raise NotImplementedError

    def save_config(self, data):
        raise NotImplementedError

# Implement JSON storage
class JSONStorage(StorageBackend):
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.file_path.touch(exist_ok=True)
        if self.file_path.stat().st_size == 0:
            self.save_config({})  # Initialize with empty JSON

    def load_config(self):
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_config(self, data):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

# Initialize FastAPI app and storage
app = FastAPI()
storage = JSONStorage("config.json")

@app.get("/agents")
def get_agents():
    config = storage.load_config()
    return config.get("agents", [])

@app.post("/agents")
def add_agent(agent: dict):
    config = storage.load_config()
    if "agents" not in config:
        config["agents"] = []
    config["agents"].append(agent)
    storage.save_config(config)
    return {"message": "Agent added successfully"}

@app.get("/tools")
def get_tools():
    config = storage.load_config()
    return config.get("tools", [])

@app.post("/tools")
def add_tool(tool: dict):
    config = storage.load_config()
    if "tools" not in config:
        config["tools"] = []
    config["tools"].append(tool)
    storage.save_config(config)
    return {"message": "Tool added successfully"}
