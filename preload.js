const { contextBridge, ipcRenderer } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  igFollow: (tf, scroll, max_f, min_f, min_p) =>
    ipcRenderer.send("ig-follow", tf, scroll, max_f, min_f, min_p),
  liConnect: (keyowords, pages) =>
    ipcRenderer.send("li-connect", keyowords, pages),
  fbInvite: (id, scroll) => ipcRenderer.send("fb-invite", id, scroll),
  fbUnfriend: () => ipcRenderer.send("fb-unfriend"),
  txFollow: () => ipcRenderer.send("tx-follow"),
});
