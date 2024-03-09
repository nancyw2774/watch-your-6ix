from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send
from picamera2 import Picamera2
import cv2
import time
from object_detection import Yolo
from camera import Camera

app = Flask(__name__)
socketio = SocketIO(app)

def gen_frames(): 
    cam = Camera()
    cam.start()
    start_time = time.time()
    while time.time() - start_time < 30:
        frame = cam.capture_array()
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

app = Flask(__name__)

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
    cam = Camera()
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


if __name__ == '__main__':
    yolo = Yolo()
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
