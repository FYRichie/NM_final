from typing import Any
from threading import Thread
from queue import Queue
from paho.mqtt import client as mqtt

from logger import Logger

# defines topic types
TOPIC = "sleep"
RESET = "4"
INIT = "init"
STATE_1 = "1"
STATE_2 = "2"
STATE_3 = "3"


class JetsonPublisher:
    """
    Mqtt publisher for Jetson Nano to send message to ESP
    """

    def __init__(self, ip: str, port: int, logger: Logger) -> None:
        """
        ip: Jetson ip
        port: Jetson port
        """
        self.client = mqtt.Client()
        self.client.connect(host=ip, port=port)
        self.client.loop_start()

    def send(self, topic: str, payload: Any) -> None:
        """
        Send message to ESP

        topic: mqtt topic
        payload: other message
        """
        self.client.publish(topic=topic, payload=payload)


class ESPConnecter:
    """
    Use mqtt to communicate with ESP module
    """

    def __init__(self, msg_queue: Queue, logger: Logger) -> None:
        """
        msg_queue: queue for thread communication, data received from ESP is stored in this queue
        """

        self.jetson_publihser = JetsonPublisher("localhost", 1883, logger)
        self.queue = msg_queue
        self.logger = logger

    def send(self, topic: str, payload: Any = "") -> None:
        """
        Send message from Jeston Nano to ESP

        topic: mqtt topic
        payload: other information
        """
        self.jetson_publihser.send(topic, payload)
