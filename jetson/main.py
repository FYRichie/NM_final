import argparse
from queue import Queue
import socket
import time

from camera import Camera
from esp_connecter import ESPConnecter, TOPIC, RESET, INIT, STATE_1, STATE_2, STATE_3
from logger import Logger
from wsclient import WSClient
from timer import Timer


def get_ip() -> str:
    return socket.gethostbyname("localhost")


parser = argparse.ArgumentParser()
parser.add_argument("--server_ip", default="192.168.10.147", help="Ip of the web server(computer)", type=str)
parser.add_argument("--server_port", default=4000, help="Port of the web server(computer)", type=int)
parser.add_argument("--fps", default=10.0, help="Camera capture frame rate", type=float)
args = vars(parser.parse_args())

if __name__ == "__main__":
    """
    Main function
    """
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
    ws_client.start()

    current_state = INIT
    call_time = 0

    while True:
        if not camera_queue.empty():
            """
            If time matches and still sleeping, call up
            """
            _, _, _, hour, min = time.strftime("%Y %m %d %H %M").split()
            time_stamp = f"{hour}:{min}".zfill(5)
            if camera_queue.get() == Camera.SLEEPING:
                clock_list = timer.get_all()
                time_list = [t["time"] for t in clock_list]
                if time_stamp in time_list and clock_list[time_list.index(time_stamp)]["activate"] and current_state == INIT:
                    current_state = STATE_1
                    esp_connecter.send(TOPIC, current_state)
                    call_time = time.time()  # seconds
                elif current_state == STATE_1 and time.time() - call_time >= 60:  # 1 minute
                    current_state = STATE_2
                    esp_connecter.send(TOPIC, current_state)
                    call_time = time.time()
                elif current_state == STATE_2 and time.time() - call_time >= 60:  # 1 minute
                    current_state = STATE_3
                    esp_connecter.send(TOPIC, current_state)
                    call_time = time.time()
                # STATE_3 does nothing

        if not ws_queue.empty():
            msg = ws_queue.get()
            task, payload = msg["task"], msg["payload"]
            success = True

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
            elif task == Timer.RESET:
                payload = ""
                current_state = INIT
                call_time = 0
                esp_connecter.send(TOPIC, RESET)
            else:
                payload = ""

            ws_client.send(task=task, success=success, payload=payload)

        if not esp_queue.empty():
            logger.info(f"Response from ESP: {esp_queue.get()}")
