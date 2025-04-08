// src/scripts/options.js

const {
    getData,
    getRawData,
    addProcess,
    editProcess,
    removeProcess,
} = require("../../renderer.js");

const addBtn = document.getElementById("addButton");
const removeButton = document.getElementById("removeButton");
const sortingMenu = document.getElementById("sortingMenu");
const backupBtn = document.getElementById("backupBtn");
const appList = document.getElementById("appList");

if (localStorage.getItem("sorting_type") != null && sortingMenu) {
    console.log(sortingMenu.value);
    sortingMenu.value = localStorage.getItem("sorting_type");
}

document.addEventListener("DOMContentLoaded", () => {
    addBtn.addEventListener("click", function () {
        var app = document.getElementById("processName");
        var customName = document.getElementById("processCustom");

        if (app.value == "" || customName.value == "") {
            return;
        }

        addProcess([app.value, customName.value]).then((response) => {
            if (response.status == "ok") {
                console.log("Success");
                app.value = "";
                customName.value = "";
            } else {
                console.log("error");
            }
        });
    });

    removeButton.addEventListener("click", function () {
        var app = document.getElementById("processName");
        var customName = document.getElementById("processCustom");

        if (app.value == "" || customName.value == "") {
            return;
        }

        removeProcess([app.value, customName.value]).then((response) => {
            if (response.status == "ok") {
                console.log("Success");
                app.value = "";
                customName.value = "";
            } else {
                console.log("error");
            }
        });
    });

    sortingMenu.addEventListener("change", function () {
        localStorage.setItem("sorting_type", sortingMenu.value);
        elementSatusList();
    });
});

backupBtn.addEventListener("click", async function () {
    try {
        const data = await getRawData();
        var blob = new Blob([JSON.stringify(data)], { type: "text/plain" });

        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url;
        a.download = "playtime_backup.runr";
        a.click();

        URL.revokeObjectURL(url);
        a.remove();
    } catch (error) {
        console.log("Error when creating backup:", error);
    }
});

function createElement(process, status) {
    const newElem = document.createElement("div");
    status = status == "on" ? "VISIBLE" : "HIDDEN";

    newElem.innerHTML = `
    <p>${process}</p>
    <p class="${status}">${status}</p>
  `;
    const statusElem = newElem.querySelector("p:last-child");
    statusElem.addEventListener("click", clicked);

    appList.appendChild(newElem);
}

async function elementSatusList() {
    const data = await getData("get-data");
    appList.innerHTML = "";
    for (x of data) {
        createElement(x[0], x[2]);
    }
}

function clicked(event) {
    var processName = event.target.parentElement.firstElementChild.innerText;

    editProcess([processName]).then((response) => {
        if (response.status == "ok") {
            console.log("Success");
            elementSatusList();
        } else {
            console.log("error");
        }
    });
}

elementSatusList();
