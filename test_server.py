from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send

import cv2
import time
from object_detection import Yolo

app = Flask(__name__)
socketio = SocketIO(app)

yolo = Yolo()
cam = cv2.VideoCapture(0)


def gen_frames(): 
    start_time = time.time()
    while time.time() - start_time < 300:
        success, frame = cam.read()  # read the camera frame
        if not success:
            break
        else:
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
    success, im = cam.read()
    if not success:
        return "Error: Camera read failed"
    return str(yolo.hazrd_exists_instant(im))

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
    return data

@socketio.on('request_speed')
def request_speed(data):
    socketio.emit('send_notification')


socketio.run(app, host='0.0.0.0', port=5001, debug=True)