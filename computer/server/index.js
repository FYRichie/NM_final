const http = require("http");
const express = require("express");
const WebSocket = require("ws");
const Logger = require("./logger");
const { TASK } = require("./constant");

const app = express();
const server = http.createServer(app);
const wss = new WebSocket.Server({ server });
const logger = new Logger();

const PORT = 4000;
let frontendClient, jetsonClient;
const sendToFrontend = (data) => {
    frontendClient.send(JSON.stringify(data));
};
const sendToJetson = (data) => {
    jetsonClient.send(JSON.stringify(data));
};

wss.on("connection", (ws) => {
    ws.onmessage = async (message) => {
        let data = JSON.parse(message.data);
        const { client, task, payload } = data;
        logger.info(`client: ${client}, task: ${task}, payload: `);
        console.log(payload);

        // TODO
        if (client === "Jetson") {
            if (payload["success"]) {
                switch (task) {
                    case TASK.INIT:
                        jetsonClient = ws;
                        break;
                    case TASK.GET_TIME_LIST:
                        sendToFrontend({
                            task: task,
                            payload: payload,
                        });
                    default:
                        break;
                }
            } else {
                logger.error(`Jetson occurs error while doing ${task}`);
                sendToFrontend({
                    task: task,
                    payload: payload,
                });
            }
        } else if (client === "Frontend") {
            switch (task) {
                case TASK.INIT:
                    frontendClient = ws;
                    break;
                case TASK.ADD_TIME:
                    sendToJetson({
                        task: task,
                        payload: payload,
                    });
                    sendToJetson({
                        task: TASK.GET_TIME_LIST,
                        payload: "",
                    });
                    break;
                case TASK.DELETE_TIME:
                    sendToJetson({
                        task: task,
                        payload: payload,
                    });
                    sendToJetson({
                        task: TASK.GET_TIME_LIST,
                        payload: "",
                    });
                    break;
                case TASK.CHANGE_ACTIVATE:
                    sendToJetson({
                        task: task,
                        payload: payload,
                    });
                    sendToJetson({
                        task: TASK.GET_TIME_LIST,
                        payload: "",
                    });
                    break;
                case TASK.CHANGE_TIME:
                    sendToJetson({
                        task: task,
                        payload: payload,
                    });
                    sendToJetson({
                        task: TASK.GET_TIME_LIST,
                        payload: "",
                    });
                    break;
                case TASK.RESET:
                    sendToJetson({
                        task: task,
                        payload: "",
                    });
                    break;
                case TASK.GET_TIME_LIST:
                    sendToJetson({
                        task: task,
                        payload: "",
                    });
                    break;
                default:
                    break;
            }
        } else {
            logger.error(`client ${client} invalid`);
        }
    };
});

server.listen(PORT, () => {
    logger.success(`Listening on http://localhost:${PORT}`);
});
