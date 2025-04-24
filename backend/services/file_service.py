
import os
import json
from config import APPDATA_PATH, APPS_JSON, RUNTIME_FILE, LOGS_PATH

def read_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_json(filepath, data):
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

def log_message(message):
    with open(LOGS_PATH, 'a') as log_file:
        log_file.write(f"{message}\n")
