// src/scripts/options.js

const {
    getData,
    addProcess,
    editProcess,
    removeProcess,
} = require("../renderer.js");

const addBtn = document.getElementById("addButton");
const removeButton = document.getElementById("removeButton");
const sortingBtn = document.getElementById("sortingBtn");
const appList = document.getElementById("appList");

if (localStorage.getItem("sorting_type") != null) {
    sortingBtn.value = localStorage.getItem("sorting_type");
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

    sortingBtn.addEventListener("click", function () {
        if (sortingBtn.value == "BIGGER") {
            localStorage.setItem("sorting_type", "LOWER");
            sortingBtn.value = "LOWER";
        } else if (sortingBtn.value == "LOWER") {
            localStorage.setItem("sorting_type", "ALPHABETICAL");
            sortingBtn.value = "ALPHABETICAL";
        } else {
            localStorage.setItem("sorting_type", "BIGGER");
            sortingBtn.value = "BIGGER";
        }
        elementSatusList()
    });
})

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

