import cv2
from ultralytics import YOLO
import math
import time

class Yolo():

    def __init__(self):
        self.model = YOLO("yolo-Weights/yolov8n.pt")
        self.class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck"]
    
    def hazrd_exists_instant(self, im, debug=False):
        results = self.model(im, stream=True)

        for r in results:
            boxes = r.boxes

            for box in boxes:
                if int(box.cls[0]) >= 2 and int(box.cls[0]) < len(self.class_names):

                    if debug:
                        # bounding box
                        x1, y1, x2, y2 = box.xyxy[0]
                        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2) # convert to int values

                        # put box in cam
                        cv2.rectangle(im, (x1, y1), (x2, y2), (255, 0, 255), 3)

                        # confidence
                        confidence = math.ceil((box.conf[0]*100))/100
                        # print("Confidence --->",confidence)

                        # class name
                        cls = int(box.cls[0])
                        # print("Class name -->", classNames[cls])

                        # object details
                        org = [x1, y1]
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        fontScale = 1
                        color = (255, 0, 0)
                        thickness = 2

                        cv2.putText(im, self.class_names[cls], org, font, fontScale, color, thickness)

                        # Display frames in a window  
                        cv2.imshow('image', im)
                    return True
        return False