from flask import Flask, request, render_template, Response
from werkzeug.utils import secure_filename
import io
from ultralytics import YOLO
import numpy as np
import cv2
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder="templates")

# Enable CORS for all routes
CORS(app)

class Detection:
    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def predict(self, img, classes=[], conf=0.5):
        if classes:
            results = self.model.predict(img, classes=classes, conf=conf)
        else:
            results = self.model.predict(img, conf=conf)
        return results

    def predict_and_detect(self, img, classes=[], conf=0.5, rectangle_thickness=3, text_thickness=2):
        results = self.predict(img, classes, conf=conf)
        for result in results:
            for box in result.boxes:
                cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),
                              (int(box.xyxy[0][2]), int(box.xyxy[0][3])), (255, 0, 0), rectangle_thickness)
                cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                            (int(box.xyxy[0][0]), int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), text_thickness)
        return img, results

    def detect_from_image(self, image):
        result_img, _ = self.predict_and_detect(image, classes=[], conf=0.5)
        return result_img

detection = Detection()

@app.route('/display_image')
def display_image():
    # Serve the saved image
    image_path = os.path.join("server", "saved", "last_frame.jpg")
    return Response(open(image_path, 'rb').read(), mimetype='image/jpeg')

@app.route('/')
def index_video():
    return render_template('video.html')

# Global variables for tracking the state of detection and the last frame
is_running = True
last_frame = None
last_detection = None

def gen_frames():
    global is_running, last_frame, last_detection
    cap = cv2.VideoCapture(1)
    while cap.isOpened():
        if not is_running:
            # If not running, just keep sending the last frame
            if last_frame is not None:
                ret, buffer = cv2.imencode('.jpg', last_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            break

        ret, frame = cap.read()
        frame = cv2.resize(frame, (512, 512))
        if frame is None:
            break

        # Apply object detection to the frame
        frame, detections = detection.predict_and_detect(frame)

        # Save the last detected frame and detection results
        last_frame = frame
        last_detection = detections

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stop_detection', methods=["POST"])
@cross_origin()
def stop_detection():
    global last_frame
    print("Saving the last frame...")  # Debug statement

    # Save the last frame if it exists
    if last_frame is not None:
        image_path = os.path.join("server", "saved", "last_frame.jpg")
        cv2.imwrite(image_path, last_frame)  # Save the last frame
        print(f"Last frame saved at {image_path}")
    else:
        print("No frame to save.")  # Debug statement if last_frame is None

    return "Last Frame Saved", 200

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)