const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let pythonProcess = null;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 1200,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    }
  });

  mainWindow.loadFile('./site/site_main.html');

  mainWindow.on('closed', function () {
    mainWindow = null;
  });
}

app.on('ready', () => {
  pythonProcess = spawn('python', ['./EventScraperJP.py'])
  createWindow();
  pythonProcess.stdout.on('data', (data) => {
    console.log(data.toString());
    mainWindow.webContents.send('childoutput', data.toString());
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('quit', function () {
  if (pythonProcess) {
    pythonProcess.kill();
}});