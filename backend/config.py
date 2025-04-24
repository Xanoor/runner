import os

if os.name == 'nt':
    APPDATA_PATH = os.path.join(os.getenv("APPDATA"), "RunnerApp")
    CONFIG_FILE = os.path.join(APPDATA_PATH, 'config.ini')
else:
    APPDATA_PATH = os.path.expanduser("~/.local/share/RunnerApp")
    CONFIG_FILE = os.path.join(APPDATA_PATH, 'config.conf')

LOGS_PATH = os.path.join(APPDATA_PATH, "logs.txt")
APPS_JSON = os.path.join(APPDATA_PATH, "apps.json")
RUNTIME_FILE = os.path.join(APPDATA_PATH, "runtime.runr")

# To improve !