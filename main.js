const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');
const kill = require('tree-kill');
const ps = require('ps-node');
const pids = [];

let mainWindow;
let pythonProcess = null;

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
    pids.forEach(function(pid) {
      // A simple pid lookup
      ps.kill( pid, function( err ) {
          if (err) {
              throw new Error( err );
          }
          else {
              console.log( 'Process %s has been killed!', pid );
          }
      });
    });
    mainWindow = null;
  });

  mainWindow.on('close', function () {
    pids.forEach(function(pid) {
      // A simple pid lookup
      ps.kill( pid, function( err ) {
          if (err) {
              throw new Error( err );
          }
          else {
              console.log( 'Process %s has been killed!', pid );
          }
      });
    });
  });
}

function killEventScraperProcess() {
  const processName = "EventScraperJP.exe";
  exec(`tasklist`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error getting the process list: ${error.message}`);
      return;
    }
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return;
    }
    if (stdout.includes(processName)) {
      console.log(`Found process ${processName}, closing...`);
      exec(`taskkill /F /IM ${processName} /T`, (killError, killStdout, killStderr) => {
        if (killError) {
          console.error(`Error closing the process: ${killError.message}`);
          return;
        }
        console.log(`Process ${processName} has been closed.`);
      });
    } else {
      console.log(`Process ${processName} hasn't been running.`);
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
    pythonProcess = spawn(pythonExePath);
    pids.push(pythonProcess.pid);
  }
  createWindow();
  if (pythonProcess) {
    pythonProcess.stdout.on('data', (data) => {
      console.log(data.toString());
      mainWindow.webContents.send('childoutput', data.toString());
    });
  }
});

app.on('window-all-closed', function () {
  pids.forEach(function(pid) {
    // A simple pid lookup
    ps.kill( pid, function( err ) {
        if (err) {
            throw new Error( err );
        }
        else {
            console.log( 'Process %s has been killed!', pid );
        }
    });
  });
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', function () {
  if (mainWindow === null) {
    createWindow();
  }
});

app.on('before-quit', function() {
  pids.forEach(function(pid) {
    // A simple pid lookup
    ps.kill( pid, function( err ) {
        if (err) {
            throw new Error( err );
        }
        else {
            console.log( 'Process %s has been killed!', pid );
        }
    });
  });
});

app.on('quit', function () {
  pids.forEach(function(pid) {
    // A simple pid lookup
    ps.kill( pid, function( err ) {
        if (err) {
            throw new Error( err );
        }
        else {
            console.log( 'Process %s has been killed!', pid );
        }
    });
  });
});