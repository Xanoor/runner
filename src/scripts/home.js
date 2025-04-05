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

    //To Paris Time -> Soon in a .ini file !
    const now = new Date();
    const formattedDate = now
        .toLocaleString("fr-FR", {
            timeZone: "Europe/Paris",
            hour12: false,
        })
        .replace(",", "");
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
