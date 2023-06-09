import cv2
from time import sleep

from app.constants import CAMERA_GPIO
from app.controller import BaseController
from app.utils import Environment

RETRIES = 5


class CameraController(BaseController):
    env = Environment()

    def __init__(self):
        print(f"Connecting the camera on channel {CAMERA_GPIO}")
        if self.env.is_live:
            camera = cv2.VideoCapture(CAMERA_GPIO)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
            super().__init__(camera, CAMERA_GPIO)
        else:
            super().__init__(None, CAMERA_GPIO)
        self.frame = None
        self.read_frame()

    def read_frame(self):
        retry_count = 1
        while True:
            if self.env.is_live:
                ret, new_frame = self.connector.read()
            else:
                ret, new_frame = True, None
            retry_count += 1
            if ret:
                break
            elif retry_count > RETRIES:
                print("Failed to read_frame from camera")
            # sleep(0.05)

        # self.frame = cv2.rotate(new_frame, cv2.ROTATE_90_CLOCKWISE)
        self.frame = new_frame
        return self.frame

    @property
    def current_frame(self):
        return self.frame

    def display_current_frame(self):
        if self.env.is_live:
            # Display the frame using Matplotlib
            cv2.imshow("Camera feed", self.current_frame)
            cv2.waitKey(1)

    def stop(self):
        print(f"Disconnecting the camera on channel {self.channel}")
        if self.env.is_live:
            self.connector.release()
            cv2.destroyAllWindows()
