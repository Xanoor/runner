# backend/services/app_service.py

import datetime
import json
from config import APPDATA_PATH, APPS_JSON, RUNTIME_FILE
from services.process_service import get_running_processes
from services.file_service import read_json, write_json, log_message

authorized_apps = set()
apps_list = []
timeframes = []
replace_dict = {}

def read_data(start=False):
    global authorized_apps, apps_list, replace_dict, timeframes
    authorized_apps = {"Runner"}
    apps_list = []
    timeframes = []
    replace_dict = {}

    data = read_json(APPS_JSON)

    for entry in data:
        process = entry.get("process", "")
        custom_name = entry.get("customName", "")
        if process and custom_name:
            authorized_apps.add(custom_name)
            replace_dict[process] = custom_name

    if start:
        log_message(f"App [RUNR] is open at [{datetime.datetime.now()}]\n")

    runtime = read_json(RUNTIME_FILE)
    if "apps" in runtime:
        for entry in runtime["apps"]:
            if entry["process"] in authorized_apps:
                apps_list.append([entry["process"], entry["runtime"], entry["status"]])

    date_str = datetime.datetime.now().strftime("%m/%Y")
    found = False
    if "timeframes" in runtime:
        for tf in runtime["timeframes"]:
            timeframes.append([tf["date"], tf["runtime"]])
            if tf["date"] == date_str:
                found = True
    if not found:
        timeframes.append([date_str, 0])

def update_apps():
    global apps_list, timeframes
    new_list = get_running_processes(authorized_apps, replace_dict)
    date_str = datetime.datetime.now().strftime("%m/%Y")

    for proc in new_list:
        found = False
        for i, app in enumerate(apps_list):
            if app[0] == proc:
                apps_list[i][1] += 2
                found = True
                break
        if not found:
            apps_list.append([proc, 0, "on"])

    for tf in timeframes:
        if tf[0] == date_str:
            tf[1] += 2

    update_app_list()

def update_app_list():
    apps = [{"process": p[0], "runtime": p[1], "status": p[2]} for p in apps_list]
    time_data = [{"date": t[0], "runtime": t[1]} for t in {t[0]: t for t in timeframes}.values()]
    write_json(RUNTIME_FILE, {"apps": apps, "timeframes": time_data})

def get_data(type):
    update_app_list()
    if type == "timeframes":
        return timeframes
    return apps_list

def update_data():
    update_apps()
    return apps_list

def get_raw_data():
    try:
        with open(RUNTIME_FILE, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found", 404
    except json.JSONDecodeError:
        return "JSON decoding error", 500

def add_process(data):
    process_name, custom_name = data[0], data[1]
    if not process_name.lower().endswith(".exe"):
        process_name += ".exe"
    apps = read_json(APPS_JSON)
    apps.append({"process": process_name, "customName": custom_name})
    write_json(APPS_JSON, apps)
    read_data()
    return {"status": "ok", "message": "Process added successfully"}

def remove_process(data):
    process_name, custom_name = data[0], data[1]
    if not process_name.endswith(".exe"):
        process_name += ".exe"
    apps = read_json(APPS_JSON)
    apps = [a for a in apps if a["process"] != process_name and a["customName"] != custom_name]
    write_json(APPS_JSON, apps)
    read_data()
    return {"status": "ok", "message": f"Process {process_name} removed successfully"}

def edit_status(proc_name):
    for i in range(len(apps_list)):
        if proc_name in apps_list[i]:
            apps_list[i][2] = "on" if apps_list[i][2] == "off" else "off"
    update_app_list()
    return {"status": "ok", "message": "Process status edited"}
