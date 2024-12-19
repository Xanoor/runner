// src/preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  fetchData: () => ipcRenderer.invoke('fetch-data'), 
});
