// src/scripts/home.js

const { getData } = require("../renderer.js");

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
        console.log(`${i[0]} data`);
    }
}

async function getPlaytimeData() {
    const data = await getData("get-data");
    createPlaytimeList(data);
}

//Init, then getData every 2minutes
getPlaytimeData();
setInterval(() => {
    getPlaytimeData();
}, 100000);
