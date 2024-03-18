from picamera2 import Picamera2, Preview
from libcamera import Transform
import cv2


cam = Picamera2()
# config = cam.create_video_configuration(transform=Transform(hflip=1))
# cam.configure(config)
cam.start()
cam.start_and_record_video("test.mp4", duration=2)