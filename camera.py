from picamera import PiCamera
import time 

camera = PiCamera()

camera.resolution = (640, 480)
camera.start_recording("test_video.h264")
camera.wait_recording(60)
camera.stop_recording()