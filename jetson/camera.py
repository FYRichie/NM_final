from asyncio.log import logger
from queue import Queue
from threading import Thread
import cv2
import time
import boto3
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
        pipeline = (
            "nvarguscamerasrc ! "
                "video/x-raw(memory:NVMM), "
                "width=(int)1920, height=(int)1080, "
                "format=(string)NV12, framerate=(fraction)30/1 ! "
            "queue ! "
            "nvvidconv flip-method=2 ! "
                "video/x-raw, "
                "width=(int)1920, height=(int)1080, "
                "format=(string)BGRx, framerate=(fraction)30/1 ! "
            "videoconvert ! "
                "video/x-raw, format=(string)BGR ! "
            "appsink"
        )

        self.camera = cv2.VideoCapture(pipeline, cv2.CAP_GSTREAMER)
        self.logger = logger
        self.queue = msg_queue
        self.fps = fps

    def __aws_service(self, img: np.ndarray) -> str:
        """
        Perform AWS deep learning to detect whether the person is sleeping or not

        img: current image captured by the camera
        """
        # TODO(Yaoting): AWS service
        client = boto3.client('rekognition',
            aws_access_key_id = "AKIAXO5ADXIIJGWB3H5T",
            aws_secret_access_key = "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"
        )

        frame = cv2.resize(img, (480, 270))
        img_str = cv2.imencode('.jpg', frame)[1].tobytes()

        response = client.detect_faces(
            Image = {
                'Bytes': img_str,
            },
            Attributes = ['ALL']
        )
        
        FaceDetails = response['FaceDetails']
        if FaceDetails != []:
            if FaceDetails[0]['EyesOpen']['Value'] == False:
                print('sleeping')
                return "sleeping"
            else :
                print('wakeup')
                return "wakeup"
        else :
            print('wakeup')
            return "wakeup"

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
