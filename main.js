const { app, BrowserWindow, ipcMain } = require("electron/main");
const { spawn, exec } = require("child_process");
const path = require("path");
const fs = require("fs");

// Logging Functions __{(for debugging)}__
function clearLogFile() {
  fs.writeFile(path.join(__dirname, "logs.txt"), "", (err) => {
    if (err) {
      console.error("Failed to clear log file:", err);
    }
  });
}
function log(message) {
  const now = new Date();
  const formatNumber = (num) => num.toString().padStart(2, "0");

  const timestampedMessage = `${[
    now.getDate(),
    now.getMonth() + 1,
    now.getFullYear(),
  ]
    .map(formatNumber)
    .join("-")} ${[now.getHours(), now.getMinutes(), now.getSeconds()]
    .map(formatNumber)
    .join(":")} - ${message}`;

  fs.appendFile(
    path.join(__dirname, "logs.txt"),
    timestampedMessage + "\n",
    (err) => {
      if (err) console.error("Failed to write to log file:", err);
    }
  );
}

// Functions for Execute Script
function execPyScript(path, args, indentifier) {
  const process = spawn("python", [path, ...args]);
  process.stdout.on("data", (data) => {
    log(`${indentifier}: ${data}`);
  });
  process.stderr.on("data", (data) => {
    log(`${indentifier} Error: ${data}`);
  });
  process.on("close", (code) => {
    if (code !== 0) {
      log(`${indentifier} Python script failed with code ${code}`);
    }
  });
}
function execChromeProfile() {
  exec(
    '"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --user-data-dir="E:\\Orion\\__chrome_data__\\default" --remote-debugging-port=9111 --no-first-run --no-default-browser-check',
    (error, stdout, stderr) => {
      if (error) {
        log(`Chrome Error: ${error.message}`);
      }
      if (stderr) {
        log(`Chrome Warn: ${stderr}`);
      }
      log(`Chrome Output: ${stdout}`);
    }
  );
}

let win;
function createWindow() {
  clearLogFile();
  win = new BrowserWindow({
    width: 800,
    height: 600,
    icon: path.join(__dirname, "app", "favicon.png"),
    autoHideMenuBar: true,
    webPreferences: {
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  const htmlPath = path.join(__dirname, "app", "index.html");
  win.loadFile(htmlPath);

  // Start up functions
  execPyScript(
    path.join(__dirname, "python", "tts.py"),
    ["Ready to go!"],
    "TTS"
  );
  execPyScript(
    path.join(__dirname, "python", "sr.py"),
    [],
    "Speech Recognition"
  );

  // IPC Communication
  ipcMain.on("ig-follow", (e, tf, scroll, max_f, min_f, min_p) => {
    execChromeProfile();
    execPyScript(
      path.join(__dirname, "python", "auto", "ig_follow.py"),
      [tf, scroll, max_f, min_f, min_p],
      "IG Follow"
    );
  });
  ipcMain.on("li-connect", (e, keyowords, pages) => {
    execChromeProfile();
    execPyScript(
      path.join(__dirname, "python", "auto", "li_connect.py"),
      [keyowords, pages],
      "LI Connect"
    );
  });
  ipcMain.on("fb-invite", (e, id, scroll) => {
    execChromeProfile();
    execPyScript(
      path.join(__dirname, "python", "auto", "fb_invite.py"),
      [id, scroll],
      "FB Invite"
    );
  });
  ipcMain.on("fb-unfriend", (e) => {
    execChromeProfile();
    execPyScript(
      path.join(__dirname, "python", "auto", "fb_unfriend.py"),
      [],
      "FB Unfriend"
    );
  });
  ipcMain.on("tx-follow", (e) => {
    execChromeProfile();
    execPyScript(
      path.join(__dirname, "python", "auto", "x_follow.py"),
      [],
      "TX Follow"
    );
  });
}

app.whenReady().then(() => createWindow());
app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});
app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow();
});
