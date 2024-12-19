from flask import Flask, jsonify
from cryptography.fernet import Fernet
import psutil
import datetime
import re

def genFernet():
    with open("data/fernet.txt", "rb+") as f:
        content = f.read().strip()
        if len(content) != 44:
            key = Fernet.generate_key()
            f.seek(0)
            f.write(key)
            f.truncate()
        else:
            key = content
    return Fernet(key)

fernet = genFernet()


app = Flask(__name__)
authorizedApps = ["runner"]
appsList = []

replaceDict = {}

@app.route('/get-data', methods=['GET'])
def get_data():
    updateApps()
    return jsonify(appsList)


def readData():
    with open('data/apps.csv', 'r') as acsv:
        for i in acsv:
            i = i.split(':')
            if (len(i) > 1):    
                customAppName = re.sub(r"(?i)\.exe", "", i[1].rstrip())
                authorizedApps.append(customAppName)
                replaceDict[i[0]] = customAppName
            else:
                authorizedApps.append(re.sub(r"(?i)\.exe", "", i[0].rstrip()))


    with open("data/logs.txt", "a") as logs:
        logs.write(f'App [RUNR] is open at [{datetime.datetime.now()}]\n')

    with open('data/playtime.runr', 'r+') as f:
        for i in f:
            i = fernet.decrypt(i.strip().encode()).decode()
            i = i.split(':')
            print(i)
            if len(i) == 3 and i[0] in authorizedApps:
                appsList.append([i[0], i[1], i[2]])
readData()

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
            appsList[index][1] = int(appData[1])+2
        elif i in authorizedApps:
            appsList.append([i, 0, 'on'])

    updateAppList()

def updateAppList():
    with open("data/playtime.runr", "w") as f:
        for i in appsList:
            data = f"{i[0]}:{i[1]}:{i[2]}"
            f.write(f'{fernet.encrypt(data.encode()).decode()}\n')  


# Iterate over all running process
def getProcess(auth:list, replaceDict:dict):
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
            with open("data/logs.txt", "a") as logs:
                logs.write(f'{runningProcess[i]} is open [{datetime.datetime.now()}]\n')
    return runningProcess

# updateApps()

if __name__ == '__main__':
    app.run(port=5000) 
