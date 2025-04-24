
import psutil
import re
from config import LOGS_PATH
from services.file_service import log_message

def get_running_processes(authorized, replace_dict):
    running = []
    for proc in psutil.process_iter(['name']):
        try:
            name = proc.info['name']
            if name:
                running.append(name)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    unique_processes = list(set(running))
    result = []

    for proc in unique_processes:
        base_name = replace_dict.get(proc, re.sub(r"(?i)\\.exe", "", proc.strip()))
        if base_name in authorized:
            result.append(base_name)
            log_message(f"{base_name} is open")
    
    return result
