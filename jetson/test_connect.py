import argparse
from queue import Queue
import time

from esp_connecter import ESPConnecter
from logger import Logger

if __name__ == "__main__":
    logger = Logger()
    esp_queue = Queue()
    esp_connecter = ESPConnecter(
        logger=logger,
        msg_queue=esp_queue
    )

    while True:
        topic = "sleep"
        payload = input("Payload: ")
        esp_connecter.send(topic, payload)

        if payload == "close":
            break