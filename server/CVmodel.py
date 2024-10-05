from flask import Flask, request, render_template, send_file, Response
from werkzeug.utils import secure_filename
import io
from ultralytics import YOLO
import numpy as np
from PIL import Image
import cv2
import os

app = Flask(__name__,template_folder="templates")
app.config['UPLOAD_FOLDER'] = 'uploads/'


class Detection:
    def __init__(self):
        #download weights from here:https://github.com/ultralytics/ultralytics and change the path
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


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/object-detection/', methods=['POST'])
def apply_detection():
    if 'image' not in request.files:
        return 'No file part'

    file = request.files['image']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        img = Image.open(file_path).convert("RGB")
        img = np.array(img)
        img = cv2.resize(img, (512, 512))
        img = detection.detect_from_image(img)
        output = Image.fromarray(img)
        buf = io.BytesIO()
        output.save(buf, format="PNG")
        buf.seek(0)
        os.remove(file_path)
        return send_file(buf, mimetype='image/png')
    


@app.route('/')
def index_video():
    return render_template('video.html')

is_running = True
last_frame = None
last_detection = None





def gen_frames():
    global is_running, last_frame, last_detection
    cap = cv2.VideoCapture(1)
    while cap.isOpened():
        if not is_running:
            if last_frame is not None:
                ret,buffer = cv2.imencode('.jpg', last_frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            break

        ret, frame = cap.read()
        frame = cv2.resize(frame, (512, 512))
        if frame is None:
            break
        frame, detections = detection.predict_and_detect(frame)

        # Save the last detected frame and detection results
        last_frame = frame
        last_detection = detections  # Save the detection results

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/stop_detection', methods = ["post"])
def stop_detection():
    global is_running
    is_running = False
    return "Detection Stopped"

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/last_detection')
def get_last_detection():
    global last_frame, last_detection
    if last_frame is not None and last_detection is not None:
        # Print out the last detected item
        for result in last_detection:
            for box in result.boxes:
                class_id = int(box.cls[0])  # Class index
                confidence = box.conf[0]    # Confidence score
                class_name = result.names[class_id]  # Class name
        # Return the last frame as an image
        ret, buffer = cv2.imencode('.jpg', last_frame)
        return Response(buffer.tobytes(), mimetype='image/jpeg')
    else:
        return "No detection available", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
    #http://localhost:8000/video for video source
    #http://localhost:8000 for image source