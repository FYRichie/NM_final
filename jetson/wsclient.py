from queue import Queue
import websocket
import json
import sys
import os
from threading import Thread
import time
from typing import Any

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")

from logger import Logger
from task import TASK


class WSClient:
    """
    Websocket client, connection between Jetson Nano and the server on computer
    """

    def __init__(self, server_ip: str, server_port: int, logger: Logger, msg_queue: Queue) -> None:
        self.url = f"ws://{server_ip}:{server_port}"
        self.ws = websocket.WebSocketApp(url=self.url, on_open=self.__on_open, on_message=self.__on_message, on_error=self.__on_error, on_close=self.__on_close)
        self.logger = logger
        self.queue = msg_queue

    def __msg_check(self, msg: dict) -> bool:
        """
        Check if message is in valid format

        msg: message in dictionary
        """
        task = msg["task"]
        payload = msg["payload"]
        return task in TASK

    def __on_open(self, ws):
        self.logger.success(f"Connected to {self.url}")
        self.send("init", True)

    def __on_message(self, ws, msg):
        self.logger.info(f"Message from server: {msg}")
        try:
            msg = json.loads(msg)
            if self.__msg_check(msg):
                self.queue.put(msg)
            else:
                self.logger.error(f"Invalid message format: {msg}")
        except:
            self.logger.error("Invalid json format")

    def __on_close(self, ws):
        self.logger.info(f"Websocket client closing")

    def __on_error(self, ws, error):
        self.logger.error(f"Websocket client error: {error}")

    def __start(self):
        """
        Start websocket client
        """
        while True:
            try:
                self.ws.run_forever()
                time.sleep(3)
            except websocket.WebSocketException:
                self.logger.error(f"Websocket client failed to connect")

    def start(self):
        client_thread = Thread(target=self.__start)
        client_thread.start()
        self.logger.success("Websocket client started")

    def send(self, task: str, success: bool, payload: Any = ""):
        """
        Send message to server

        msg: message to send
        """
        self.ws.send(json.dumps({"client": "Jetson", "task": task, "payload": {"success": success, "data": payload}}))
