// src/index.js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const started = require('electron-squirrel-startup'); // Pour la gestion des installations

// Importer axios dans le processus principal
const axios = require('axios');

// Si l'application a été lancée par le gestionnaire d'installation (par exemple après une mise à jour),
if (started) {
  app.quit(); // Quitter l'application immédiatement pour éviter qu'elle ne démarre deux fois
}

// Cette fonction crée la fenêtre principale de l'application.
const createWindow = () => {
  // Crée la fenêtre du navigateur.
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'), 
      contextIsolation: true, 
      nodeIntegration: false, 
    },
  });

  mainWindow.loadFile(path.join(__dirname, 'index.html'));

  // mainWindow.webContents.openDevTools();
};


app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});


app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});


ipcMain.handle('fetch-data', async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/get-data'); 
    return response.data; 
  } catch (error) {
    console.error('Error fetching data:', error);
    throw error; 
  }
});

