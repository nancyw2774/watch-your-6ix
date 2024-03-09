from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send

import cv2
import time
from object_detection import Yolo
from picamera2 import Picamera2



app = Flask(__name__)
socketio = SocketIO(app)

yolo = Yolo()
cam = None

speed = 0
speed_updated = False

def gen_frames(): 
    start_time = time.time()
    while time.time() - start_time < 300:
        frame = cam.capture_array()  # read the camera frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/trigger_event/<int:level>')
def trigger_event(level):
    print(level)
    if level == 1:
        socketio.emit('send_notification', {'message': 'green', 'trafficLight': 1})
    elif level == 2:
        socketio.emit('send_notification', {'message': 'yellow', 'trafficLight': 2})
    elif level == 3:
        socketio.emit('send_notification', {'message': 'red', 'trafficLight': 3})
    elif level == 0:
        socketio.emit('send_notification', {'message': 'off', 'trafficLight': 0})
    elif level == 4:
        socketio.emit('send_notification', {'message': 'Enable Camera', 'trafficLight': 0})
    elif level == 5:
        socketio.emit('send_notification', {'message': 'Disable Camera', 'trafficLight': 0})
    else:
        socketio.emit('send_notification', {'message': 'New Notification', 'trafficLight': 0})
    # socketio.emit('trigger_event')
    print("done")
    return "Success"

@app.route('/has_hazard')
def has_hazard():
    im = cam.capture_array()

    return str(yolo.hazrd_exists_instant(im[:, :, :3]))

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('send_notification')
def send_notification(data):
    message = data.get('message', 'Default Notification')
    send({'message': message}, broadcast=True)

@socketio.on('speed_data')
def speed_data(data):
    global speed_updated
    global speed
    speed_updated = True
    speed = data

@socketio.on('request_speed')
def request_speed():
    global speed_updated
    speed_updated = False
    socketio.emit('send_notification')

def get_speed():
    request_speed()
    timeout = 5
    start_time = time.perf_counter()
    while True:
        if time.perf_counter() - start_time > timeout:
            return None
        if speed_updated:
            return speed

try:
    cam = Picamera2()
    cam.start()
    print("Camera initialized")
except:
    print("Camera busy")


socketio.run(app, host='0.0.0.0', port=5001)