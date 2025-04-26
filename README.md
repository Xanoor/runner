# Runner 🎯

Runner is a personal project designed to track the total runtime of specific processes on your system. Built as an Electron application with a Python Flask backend, it records and logs process usage durations.

**Note:** This project is a personal experiment and is not meant for commercial use or as a polished release.

---

## Features ✨

-   Tracks the total runtime of selected processes & timeframes.
-   Allows users to add, remove, and manage processes.
-   Logs process activity and saves data locally.
-   Provides a periodic data update mechanism.

---

## 🚀 Tech stack

![Electron.js](https://img.shields.io/badge/Electron-191970?style=for-the-badge&logo=Electron&logoColor=white)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

---

## Installation 🛠️

-   [Node.js](https://nodejs.org/) (for running Electron)
-   [Python 3.x](https://www.python.org/) (for the Flask backend)

1. Clone the repository:

```bash
git clone https://github.com/Xanoor/runner.git
cd runner
```

2. Install the Node.js dependencies and the required Python libraries with:

```bash
npm install
```

```bash
pip install flask psutil
```

-   Ensure the required Python libraries are installed.

---

## Usage 🚀

> ⚠️ Since an executable file (`backend.exe`) for the Flask backend is not provided in the code (`const backendPath = path.join(process.resourcesPath, "app", "src", "backend", "backend.exe");`), you may encounter an error in the console related to the backend executable when launching the app. **This error can be safely ignored**, as the Flask server is started separately in step 1.

1. Start the Flask backend:

```bash
python backend/main.py
```

2. Start the Electron app:

```bash
npm start
```

3. Ensure the following data files are created in `%APPDATA%/RunnerApp/data` (Windows) or `~/.local/share/RunnerApp/data` (Linux/Mac):

    - `runtime.runr`
    - `apps.json`
    - `logs.txt`

    The application automatically initializes these files if they don’t exist.

---

## File Structure 📂

```plaintext
.
├── LICENSE
├── README.md
├── backend
│   ├── app.py
│   ├── config.py
│   ├── init_data.py
│   ├── main.py
│   ├── routes
│   │   └── api_routes.py
│   └── services
│       ├── app_service.py
│       ├── file_service.py
│       └── process_service.py
├── package-lock.json
├── package.json
└── src
    ├── assets
    │   ├── Logo.ico
    │   ├── cross.svg
    │   ├── index.css
    │   └── options.css
    ├── backend
    │   └── runner-backend.exe
    ├── index.js
    ├── pages
    │   ├── chart.html
    │   ├── export.html
    │   ├── home.html
    │   └── options
    │       ├── appsOptions.html
    │       └── styleOptions.html
    ├── renderer.js
    └── scripts
        ├── home.js
        └── options.js
```

---

## Data Storage 💾

The following files are saved in `%APPDATA%/RunnerApp/data` (Windows) or `~/.local/share/RunnerApp/data` (Linux/Mac):

-   **`runtime.runr`**: Stores process runtime data.
-   **`apps.json`**: Contains the list of processes to track.
-   **`logs.txt`**: Logs events and activities.
-   **`config.ini`**: Config file [WINDOWS ONLY].
-   **`config.conf`**: Config file [LINUX ONLY].
