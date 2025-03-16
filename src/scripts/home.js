// src/scripts/home.js

const { getData } = require("../renderer.js");
const last_save = document.getElementById("last-save");

function newElem(name, time) {
    const newElem = document.createElement("div");
    time = `${Math.floor(time / 60)}h${time % 60}`;
    newElem.innerHTML = `
    <p>${name}</p>
    <p>${time}</p>
  `;
    return newElem;
}

function createPlaytimeList(data) {
    const playtimeList = document.getElementById("appList");
    console.log("Data received from Python:", data);
    playtimeList.innerHTML = "";

    for (let i of data) {
        playtimeList.appendChild(newElem(i[0], i[1]));
    }

    const now = new Date();
    const formattedDate = now.toISOString().slice(0, 19).replace("T", " ");
    last_save.innerText = `Last update: ${formattedDate}`;
}

async function getPlaytimeData() {
    const data = await getData("get-data");
    if (data) createPlaytimeList(data);
}

//Init, then getData every 2minutes
getPlaytimeData();
setInterval(() => {
    getPlaytimeData();
}, 100000);
