from asyncio.log import logger
from queue import Queue
from threading import Thread
import cv2
import time
import numpy as np

from logger import Logger


class Camera:
    """
    Capture image and perform pre-processing and post-processing, then send image to computer via gstreaming
    """

    SLEEPING = "sleeping"
    WAKEUP = "wakeup"

    def __init__(self, fps: float, logger: Logger, msg_queue: Queue) -> None:
        """
        fps: frame rate for judgement
        size: image size (width, height)
        """
        self.camera = cv2.VideoCapture(0)
        self.logger = logger
        self.queue = msg_queue
        self.fps = fps

    def __aws_service(self, img: np.ndarray) -> str:
        """
        Perform AWS deep learning to detect whether the person is sleeping or not

        img: current image captured by the camera
        """
        # TODO(Yaoting): AWS service

    def __start_camera(self) -> None:
        """
        Start capturing image and detecting
        """
        while True:
            ret, frame = self.camera.read()
            if not ret:
                logger.error("Camera 0 failed")
                break

            detect_result = self.__aws_service(frame)
            logger.info(f"Detection result: {detect_result}")
            while not self.queue.empty():
                self.queue.get()
            self.queue.put(detect_result)
            time.sleep(1.0 / self.fps)

        self.camera.release()

    def start(self) -> None:
        """
        Start camera
        """
        camera_thread = Thread(target=self.__start_camera)
        camera_thread.start()
        self.logger.success("Camera started")
