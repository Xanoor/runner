from flask import Flask, jsonify, request
import psutil
import datetime
import re
import json
import os

if os.name == 'nt':  # Windows
    APPDATA_PATH = os.path.join(os.getenv("APPDATA"), "RunnerApp", "data")
else:  
    APPDATA_PATH = os.path.expanduser("~/.local/share/RunnerApp/data")

if not os.path.exists(APPDATA_PATH):
    os.makedirs(APPDATA_PATH)

    logs_path = os.path.join(APPDATA_PATH, "logs.txt")
    with open(logs_path, "w") as f:
        f.write("Logs file created.\n")

    apps_path = os.path.join(APPDATA_PATH, "apps.json")
    apps_json_data = [
        {
            "process": "RunnerApp.exe",
            "customName": "Runner"
        }
    ]
    with open(apps_path, "w") as apps_json_file:
        json.dump(apps_json_data, apps_json_file, indent=4)
    
    playtime_path = os.path.join(APPDATA_PATH, "playtime.runr")
    with open(playtime_path, "w") as f:
        json.dump([], f, indent=4)


            
app = Flask(__name__)
authorizedApps = []
appsList = []

replaceDict = {}

@app.route('/')
def flaskIsRunning():
    return 'Flask is running!'

@app.route('/get-data', methods=['GET'])
def getData():
    updateAppList()
    return jsonify(appsList)

@app.route('/update-data', methods=['GET'])
def updateData():
    updateApps()
    return jsonify(appsList)

@app.route('/add-process', methods=['POST'])
def addProcess():
    processData = request.json

    data = []
    try:
        with open(os.path.join(APPDATA_PATH, 'apps.json'), 'r') as json_file:
            try:
                data = json.load(json_file) 
            except json.JSONDecodeError:
                data = [] 
    except FileNotFoundError:
        data = []

    if not processData[0].endswith(".exe"):
        processData[0] += ".exe"

    new_entry = {
        "process": processData[0],
        "customName": processData[1]
    }

    data.append(new_entry)

    with open(os.path.join(APPDATA_PATH, 'apps.json'), 'w') as json_file:
        json.dump(data, json_file, indent=4)

    readData()
    return {"status": "ok", "message": "Process added successfully"}

@app.route('/remove-process', methods=['POST'])
def removeProcess():
    processData = request.json

    data = []
    try:
        with open(os.path.join(APPDATA_PATH, 'apps.json'), 'r') as json_file:
            try:
                data = json.load(json_file) 
            except json.JSONDecodeError:
                data = [] 
    except FileNotFoundError:
        data = []

    if not processData[0].endswith(".exe"):
        processData[0] += ".exe"

    updated_data = [entry for entry in data if entry.get("process") != processData[0] and entry.get('customName') != processData[1]]

    with open(os.path.join(APPDATA_PATH, 'apps.json'), 'w') as json_file:
        json.dump(updated_data, json_file, indent=4)

    readData()
    return {"status": "ok", "message": f"Process {processData[0]} removed successfully"}

@app.route('/edit-status', methods=['POST'])
def editStatus():
    processData = request.json[0]
    for i in range(len(appsList)):
        if processData in appsList[i]:
            status = "on" if appsList[i][2] == "off" else "off"
            appsList[i][2] = status
    updateAppList()
    return {"status": "ok", "message": "Process status edited"}

def readData(start=False):
    global authorizedApps, appsList, replaceDict
    authorizedApps = ["runner"]
    appsList = []
    replaceDict = {}

    with open(os.path.join(APPDATA_PATH, 'apps.json'), 'r') as json_file:
        data = json.load(json_file)
        
        for entry in data:
            if "process" in entry and "customName" in entry:
                customAppName = re.sub(r"(?i)\.exe", "", entry['customName'].rstrip())
                authorizedApps.append(customAppName)
                replaceDict[entry['process']] = customAppName
            elif "process" in entry:
                authorizedApps.append(re.sub(r"(?i)\.exe", "", entry['app'].rstrip()))

    if start:
        with open(os.path.join(APPDATA_PATH, "logs.txt"), "a") as logs:
            logs.write(f'App [RUNR] is open at [{datetime.datetime.now()}]\n')

    with open(os.path.join(APPDATA_PATH, 'playtime.runr'), 'r+') as f:
        data = json.load(f)

        for entry in data:
            if "process" in entry and "playtime" in entry and entry["process"] in authorizedApps:
                appsList.append([entry["process"], entry["playtime"], entry['status']])

def getAppData(appName: str):
    for i in range(len(appsList)):
        if appName == appsList[i][0]:
            return True, appsList[i], i
    return False, None, 0

def updateApps():
    newList = getProcess(authorizedApps, replaceDict)

    for i in newList:
        appExist, appData, index = getAppData(i)
        if appExist:
            appsList[index][1] = int(appData[1]) + 2
        elif i in authorizedApps:
            appsList.append([i, 0, "on"])

    updateAppList()

def updateAppList():
    with open(os.path.join(APPDATA_PATH, "playtime.runr"), "w") as f:
        if len(appsList) > 1:
            data = [{"process": appData[0], "playtime": appData[1], "status": appData[2]} for appData in appsList]
            json.dump(data, f, indent=4)

def getProcess(auth: list, replaceDict: dict):
    runningProcess = []
    for proc in psutil.process_iter():
        try:
            processName = proc.name()
            runningProcess.append(processName)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    runningProcess = list(set(runningProcess))
    for i in range(len(runningProcess)):
        if runningProcess[i] in replaceDict:
            runningProcess[i] = replaceDict[runningProcess[i]]
        runningProcess[i] = re.sub(r"(?i)\.exe", "", runningProcess[i].rstrip())

        if runningProcess[i] in auth:
            with open(os.path.join(APPDATA_PATH, "logs.txt"), "a") as logs:
                logs.write(f'{runningProcess[i]} is open [{datetime.datetime.now()}]\n')
    return runningProcess

if __name__ == '__main__':
    readData(True)
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)