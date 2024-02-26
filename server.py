from flask import Flask, render_template, Response
from picamera2 import Picamera2
import cv2
import time

def gen_frames(): 
    picam2 = Picamera2()
    picam2.start()
    start_time = time.time()
    while time.time() - start_time < 30:
        frame = picam2.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

app.run(host='0.0.0.0', port=5001, debug=True)