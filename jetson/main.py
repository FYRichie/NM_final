import argparse
from queue import Queue
import socket
import time

from camera import Camera
from esp_connecter import ESPConnecter, TOPIC_TYPE
from logger import Logger
from wsclient import WSClient, MessageParser
from timer import Timer


def get_ip() -> str:
    hostname = socket.gethostname()
    return socket.gethostbyname(hostname)


if __name__ == "__main__":
    """
    Main function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("server_ip", default="192.168.10.147", help="Ip of the web server(computer)", type=str)
    parser.add_argument("server_port", default=4000, help="Port of the web server(computer)", type=int)
    parser.add_argument("esp_ip", default="192.168.10.123", help="Ip of ESP module", type=str)
    parser.add_argument("esp_port", default=3000, help="Port of ESP module", type=int)
    parser.add_argument("jetson_ip", default=get_ip(), help="Ip of Jetson Nano", type=str)
    parser.add_argument("jetson_port", default=3000, help="Port of Jetson Nano", type=int)
    parser.add_argument("fps", default=10.0, help="Camera capture frame rate", type=float)
    args = vars(parser.parse_args())

    logger = Logger()
    camera_queue = Queue(maxsize=1)
    ws_queue = Queue()
    esp_queue = Queue()

    timer = Timer(
        logger=logger,
    )
    camera = Camera(
        fps=args["fps"],
        logger=logger,
        msg_queue=camera_queue,
    )
    esp_connecter = ESPConnecter(
        jetson_ip=args["jetson_ip"],
        jetson_port=args["jetson_port"],
        esp_ip=args["esp_ip"],
        esp_port=args["esp_port"],
        logger=logger,
        msg_queue=esp_queue,
    )
    ws_client = WSClient(
        server_ip=args["server_ip"],
        server_port=args["server_port"],
        logger=logger,
        msg_queue=ws_queue,
    )

    camera.start()
    esp_connecter.listen()
    ws_client.start()

    while True:
        if not camera_queue.empty():
            """
            If time matches and still sleeping, call up
            """
            _, _, _, hour, min = time.strftime("%Y %m %d %H %M").split()
            time_stamp = f"{hour}:{min}".zfill(5)
            if time_stamp in timer.get_all() and camera_queue.get() == Camera.SLEEPING:
                esp_connecter.send(TOPIC_TYPE[0], True)

        if not ws_queue.empty():
            msg = ws_queue.get()
            task, payload = msg["task"], msg["payload"]
            success = True
            payload = ""

            if task == Timer.ADD_TIME:
                success = timer.add_time(payload)
            elif task == Timer.CHANGE_TIME:
                success = timer.change_time(payload["source_time"], payload["target_time"])
            elif task == Timer.DELETE_TIME:
                success = timer.delete_time(payload)
            elif task == Timer.CHANGE_ACTIVATE:
                success = timer.change_activate(payload)
            elif task == Timer.GET_TIME_LIST:
                payload = timer.get_all()

            ws_client.send(task=task, success=success, payload=payload)

        if not esp_queue.empty():
            logger.info(f"Response from ESP: {esp_queue.get()}")
