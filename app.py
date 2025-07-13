from flask import Flask, jsonify, send_file, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import cv2

app = Flask(__name__)
people_in_room = False  # Initially, no people in the room
captured_image_path = 'frontend/static/captured_image.jpg'  # Path to the captured image
last_captured_image_path=''

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def check_people_in_room():
    global people_in_room
    # Logic to check if people are in the room
    # Set the value of `people_in_room` accordingly

    # Capture an image using OpenCV
    capture = cv2.VideoCapture(0)  # Change the index to the appropriate camera if necessary
    _, frame = capture.read()
    capture.release()

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) > 0:
        people_in_room = True
    else:
        people_in_room = False

    # Save the captured image if people are in the room
    cv2.imwrite(captured_image_path, frame)
    

scheduler = BackgroundScheduler()
scheduler.add_job(check_people_in_room, 'interval', minutes=1)
scheduler.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/people')
def get_people_status():
    return jsonify({'people_in_room': people_in_room})

@app.route('/api/image')
def get_captured_image():
    return send_file(captured_image_path, mimetype='image/jpg')

#last_captured_image_path=captured_image_path

if __name__ == '__main__':
    app.run(debug=True)
