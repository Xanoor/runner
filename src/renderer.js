// src/renderer.js
const { ipcRenderer } = require("electron");

if (localStorage.getItem("sorting_type") == null) {
    localStorage.setItem("sorting_type", "BIGGER");
}

document.addEventListener("DOMContentLoaded", () => {
    const quitButton = document.getElementById("quit");
    if (quitButton) {
        quitButton.addEventListener("click", closeApp);
    } else {
        console.error("Quit button not found !");
    }
});

function sort_playtime(data, type) {
    if (type == "ALPHABETICAL") {
        return data.sort((a, b) => a[0].localeCompare(b[0]));
    } else if (type == "BIGGER") {
        return data.sort((a, b) => b[1] - a[1]);
    } else {
        return data.sort((a, b) => a[1] - b[1]);
    }
}

async function getData(fnc, type) {
    try {
        const data = await ipcRenderer.invoke(
            "fetch-data",
            fnc,
            type ? type : "apps"
        );
        return sort_playtime(data, localStorage.getItem("sorting_type"));
    } catch (error) {
        console.error("Error:", error);
        return [];
    }
}

async function getRawData() {
    try {
        const data = await ipcRenderer.invoke("fetch-data", "get-raw-data");
        return data;
    } catch (error) {
        console.log("Error when fetching data");
        return "";
    }
}

function addProcess(data) {
    return ipcRenderer.invoke("add-process", data);
}

function removeProcess(data) {
    return ipcRenderer.invoke("remove-process", data);
}

function editProcess(data) {
    return ipcRenderer.invoke("edit-status", data);
}

function closeApp(e) {
    e.preventDefault();
    ipcRenderer.invoke("close");
}

module.exports = {
    getData,
    getRawData,
    addProcess,
    removeProcess,
    editProcess,
};
