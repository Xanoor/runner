// src/index.js

const { app, BrowserWindow, ipcMain } = require("electron");
const path = require("path");
const { spawn } = require("child_process");
const axios = require("axios");

const backendPath = path.join(
    process.resourcesPath,
    "app",
    "src",
    "backend",
    "runner-backend.exe"
);
let backendProcess = null;
let devMode = false; // in dev mode, the backend is started separately by the developer
let backendStarted = devMode; // Variable to track if the Flask backend was successfully started
let count = 0;
// Create the main Electron window
const createWindow = () => {
    const mainWindow = new BrowserWindow({
        width: 850,
        height: 600,
        resizable: false,
        frame: false,
        icon: path.join(__dirname, "assets/Logo.ico"),
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    mainWindow.loadFile(path.join(__dirname, "pages/home.html"));

    // Uncomment this line to open the developer tools automatically
    if (devMode) mainWindow.webContents.openDevTools();
};

// Function to check if Flask is running
const waitForFlask = async (retries = 5, interval = 1000) => {
    for (let i = 0; i < retries; i++) {
        try {
            await axios.get("http://127.0.0.1:5000");
            console.log("Flask is running.");
            return true;
        } catch (error) {
            console.log(`Retrying Flask connection... (${i + 1}/${retries})`);
            await new Promise((resolve) => setTimeout(resolve, interval));
        }
    }
    console.error("Flask failed to start after multiple attempts.");
    return false;
};

// Function to fetch data from the backend
const fetchData = async (fnc) => {
    try {
        const response = await axios.get(
            `http://127.0.0.1:5000/${encodeURIComponent(fnc)}`
        );
        console.log(`Data fetched for ${fnc}:`, response.data);
        count += 1;
        console.log(count);
        return response.data;
    } catch (error) {
        if (!backendStarted)
            console.error(`Error fetching data for ${fnc}:`, error);
        else if (backendProcess && !devMode) {
            console.log("Backend process terminated.");
            app.quit();
        }
    }
};

app.whenReady().then(async () => {
    console.log("Starting Electron application...");

    // Start the Flask backend process
    try {
        const backendProcess = spawn(backendPath, {
            detached: true,
            stdio: "ignore",
        });

        backendProcess.unref();

        backendProcess.on("error", (err) => {
            console.error("Error starting the backend process:", err);
        });

        backendProcess.on("close", (code) => {
            console.log(`Backend process exited with code: ${code}`);
        });

        backendStarted = true; // Set the flag to true if the backend was successfully started
    } catch (error) {
        console.error("Error spawning the backend process:", error);
    }

    // Only proceed to wait for Flask if the backend started successfully
    if (backendStarted && !devMode) {
        try {
            const flaskReady = await waitForFlask();
            if (!flaskReady) {
                console.error("Flask backend is not ready.");
            }
        } catch (error) {
            console.error("Error while waiting for Flask to be ready:", error);
        }
    } else if (!backendProcess && !devMode) {
        console.error("Backend process did not start successfully.");
    }

    // Proceed to create the window after confirming Flask is ready
    createWindow();

    // Periodically fetch updates from the backend every 2 minutes
    setInterval(async () => {
        try {
            await fetchData("update-data");
        } catch (error) {
            console.error("Error during periodic data update:", error);
        }
    }, 120000); // 120000 ms = 2 minutes

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

// Event triggered when all windows are closed
app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        if (backendProcess) {
            backendProcess.kill("SIGINT");
            console.log("Backend process terminated.");
        }
        app.quit();
    }
});

// Handle app close request from the frontend
ipcMain.handle("close", () => {
    if (backendProcess) {
        backendProcess.kill("SIGINT");
        console.log("Backend process terminated.");
    }
    app.quit();
});

// Handle fetch-data requests from the frontend
ipcMain.handle("fetch-data", async (event, fnc) => {
    return fetchData(fnc);
});

// Add a process via Flask
ipcMain.handle("add-process", async (event, data) => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/add-process",
            data
        );
        return response.data;
    } catch (error) {
        console.error("Error adding a process:", error);
        throw error;
    }
});

// Remove a process via Flask
ipcMain.handle("remove-process", async (event, data) => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/remove-process",
            data
        );
        return response.data;
    } catch (error) {
        console.error("Error removing a process:", error);
        throw error;
    }
});

// Edit the status of a process via Flask
ipcMain.handle("edit-status", async (event, data) => {
    try {
        const response = await axios.post(
            "http://127.0.0.1:5000/edit-status",
            data
        );
        return response.data;
    } catch (error) {
        console.error("Error editing status:", error);
        throw error;
    }
});
