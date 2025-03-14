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
    json_data = {"apps": [
            {
                "process": "RunnerApp.exe",
                "customName": "Runner"
            }
        ], "timeframes": {}
    }
    with open(apps_path, "w") as apps_json_file:
        json.dump(json_data, apps_json_file, indent=4)
    
    runtime_path = os.path.join(APPDATA_PATH, "runtime.runr")
    with open(runtime_path, "w") as f:
        json.dump([], f, indent=4)



app = Flask(__name__)
authorizedApps = []
appsList = []
timeframes = []

replaceDict = {}

@app.route('/')
def flaskIsRunning():
    return 'Flask is running - RunnerApp !'

@app.route('/get-data', methods=['GET'])
def getData():
    updateAppList()
    return jsonify(appsList)

@app.route('/get-raw-data', methods=['GET'])
def getRawData():
    try:
        with open(os.path.join(APPDATA_PATH, "runtime.runr"), "r") as file:
            data = file.read()  
        return data
    
    except FileNotFoundError:
        return "File not found", 404
    except json.JSONDecodeError:
        return "JSON decoding error", 500

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

    with open(os.path.join(APPDATA_PATH, 'runtime.runr'), 'r+') as f:
        data = json.load(f)
        current_date_found = False
        date_str = datetime.datetime.now().strftime("%m/%Y")

        for entry in data["apps"]:
            if "process" in entry and "runtime" in entry and entry["process"] in authorizedApps:
                appsList.append([entry["process"], entry["runtime"], entry['status']])

        for entry in data["timeframes"]:
            if entry["date"] == date_str: current_date_found = True
            timeframes.append([entry["date"], entry["runtime"]])

        if current_date_found == False:
            timeframes.append([date_str, 0])

def getAppData(appName: str):
    for i in range(len(appsList)):
        if appName == appsList[i][0]:
            return True, appsList[i], i
    return False, None, 0

def updateApps():
    newList = getProcess(authorizedApps, replaceDict)
    date_str = datetime.datetime.now().strftime("%m/%Y")

    for i in newList:
        appExist, appData, index = getAppData(i)
        if appExist:
            appsList[index][1] = int(appData[1]) + 2
        elif i in authorizedApps:
            appsList.append([i, 0, "on"])
    for i in timeframes:
        if i[0] == date_str:
            i[1] += 2

    updateAppList()

def updateAppList():
    with open(os.path.join(APPDATA_PATH, "runtime.runr"), "w") as f:
        if len(appsList) > 1:
            apps = [{"process": appData[0], "runtime": appData[1], "status": appData[2]} for appData in appsList]
            tf = [{"date": timeframe[0], "runtime": timeframe[1]} for timeframe in timeframes]
            json_data = {
                "apps": apps,
                "timeframes": tf  
            }
            json.dump(json_data, f, indent=4)

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