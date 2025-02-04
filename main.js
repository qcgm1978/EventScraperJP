const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');

let mainWindow;
let pythonProcess = null;
let pid = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 1200,
    icon: path.join(__dirname, 'site', 'app-icon.png'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  mainWindow.loadFile('./site/site_main.html');

  mainWindow.on('closed', function () {
    if (pythonProcess) {
      exec(`taskkill /PID ${pid} /F`);
    }
    mainWindow = null;
  });

  mainWindow.on('close', function () {
    if (pythonProcess) {
      exec(`taskkill /PID ${pid} /F`);
    }
  });
}

app.on('ready', () => {
  let pythonExePath;

  if (process.env.NODE_ENV === "development") {
    // In development, run Python script normally
    pythonExePath = "python";
    pythonProcess = spawn(pythonExePath, ["./EventScraperJP.py"]);
  } else {
    // In packaged app, find the bundled .exe
    pythonExePath = path.join(process.resourcesPath, "EventScraperJP.exe");
    pythonProcess = spawn(pythonExePath, [], {detached: true});
    pid = pythonProcess.pid;
  }
  createWindow();
  if (pythonProcess) {
    pythonProcess.stdout.on('data', (data) => {
      console.log(data.toString());
      mainWindow.webContents.send('childoutput', data.toString());
    });
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('window-all-closed', function () {
  if (pythonProcess) {
    exec(`taskkill /PID ${pid} /F`);
  }
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('quit', function () {
  if (pythonProcess) {
    exec(`taskkill /PID ${pid} /F`);
  }
});