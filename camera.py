from picamera import PiCamera
import time 

camera = PiCamera()

camera.start_preview()

camera.capture("test2.jpg")