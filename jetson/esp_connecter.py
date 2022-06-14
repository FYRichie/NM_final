from typing import Any
from threading import Thread
from queue import Queue
from paho.mqtt import client as mqtt

from logger import Logger

# defines topic types
TOPIC_TYPE = ["wake"]


class ESPSubscriber:
    """
    Mqtt subscriber for listening to ESP
    """

    def __init__(self, ip: str, port: int, msg_queue: Queue, logger: Logger) -> None:
        """
        ip: ESP ip
        port: ESP port
        msg_queue: queue for thread communication, data received from ESP is stored in this queue
        """
        self.client = mqtt.Client()

        def on_message(client, obj, msg):
            """
            Procedure while receives a message from ESP
            """
            logger.info(f"TOPIC: {msg.topic}, PAYLOAD: {msg.payload}")
            msg_queue.put({"topic": msg.topic, "payload": msg.payload})

        self.client.on_message = on_message
        self.client.connect(host=ip, port=port)
        for topic in TOPIC_TYPE:
            if isinstance(topic, str):
                self.client.subscribe(topic=topic)

    def listen(self) -> None:
        """
        Start the loop
        """
        self.client.loop_forever()


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

    def __init__(self, jetson_ip: str, jetson_port: int, esp_ip: str, esp_port: int, msg_queue: Queue, logger: Logger) -> None:
        """
        jetson_ip: ip of Jetson Nano
        jetson_port: port of Jetson publisher
        esp_ip: ip of ESP
        esp_port: port of ESP publisher
        msg_queue: queue for thread communication, data received from ESP is stored in this queue
        """

        self.jetson_publihser = JetsonPublisher(jetson_ip, jetson_port, logger)
        self.esp_subscriber = ESPSubscriber(esp_ip, esp_port, msg_queue, logger)
        self.queue = msg_queue
        self.logger = logger

    def send(self, topic: str, payload: Any = "") -> None:
        """
        Send message from Jeston Nano to ESP

        topic: mqtt topic
        payload: other information
        """
        self.jetson_publihser.send(topic, payload)

    def listen(self) -> None:
        """
        Listen ESP message
        """
        connecter_thread = Thread(target=self.esp_subscriber.listen)
        connecter_thread.start()
        self.logger.success("ESP started")
