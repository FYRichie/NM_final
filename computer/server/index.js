const http = require("http");
const express = require("express");
const WebSocket = require("ws");
const prompt = require("prompt-sync")();
const Logger = require("../logger");
const { stdin, stdout } = require("process");

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });
const logger = new Logger();

const PORT = 4000;

wss.on("connection", (ws) => {
    const sendData = (data) => {
        ws.send(JSON.stringify(data));
    };

    ws.onmessage = async (message) => {
        const data = message.data;
        const [task, payload] = JSON.parse(data);

        // TODO
    };

    // testing
    while (true) {
        const task = prompt("Task: ");
        const payload = prompt("Payload: ");

        const data = {
            task: task,
            payload: payload,
        };
        if (task === "stop") {
            break;
        }
        sendData(data);
    }
});

server.listen(PORT, () => {
    logger.success(`Listening on http://localhost:${PORT}`);
});
