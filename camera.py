from picamera2 import Picamera2
import cv2

class Camera:
    def __init__(self):
        self.cam = Picamera2()

    def start(self):
        picam2.start()

    def read(self):
        return self.cam.capture_array()

#picam2 = Picamera2()
#picam2.start_and_record_video("test.mp4", duration=5)