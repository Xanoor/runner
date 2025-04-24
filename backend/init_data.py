import os, json
from config import APPDATA_PATH, LOGS_PATH, APPS_JSON, RUNTIME_FILE

def init_app_data():
    if not os.path.exists(APPDATA_PATH):
        os.makedirs(APPDATA_PATH)
        with open(LOGS_PATH, "w") as f:
            f.write("Logs file created.\n")
        with open(APPS_JSON, "w") as f:
            json.dump([{"process": "RunnerApp.exe", "customName": "Runner"}], f, indent=4)
        with open(RUNTIME_FILE, "w") as f:
            json.dump({}, f, indent=4)

# Join it to main files