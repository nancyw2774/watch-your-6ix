from flask import Flask, render_template, Response
from flask_socketio import SocketIO, send
from picamera2 import Picamera2
import cv2
import time
from object_detection import Yolo
from camera import Camera

app = Flask(__name__)
socketio = SocketIO(app)

yolo = Yolo()
cam = Camera()

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

@app.route('/trigger_event')
def test():
    socketio.emit('send_notification', {'message': 'New Notification'})
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


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)
