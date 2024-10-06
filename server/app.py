from flask import Flask, request, render_template, Response, jsonify
from werkzeug.utils import secure_filename
import io
from ultralytics import YOLO
import numpy as np
import cv2
import os
from flask_cors import CORS, cross_origin
import db
import random
import genchart

app = Flask(__name__, template_folder="templates")
CORS(app)  # Enable CORS for all routes

expiry = "88"
price = "99"
info = ""

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
                #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
                #contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                #cv2.drawContours(img, contours, -1, (0, 255, 0), 4) 
                #cv2.rectangle(img, (int(box.xyxy[0][0]), int(box.xyxy[0][1])),(int(box.xyxy[0][2]), int(box.xyxy[0][3])), (0, 255, 0), rectangle_thickness)
                cv2.putText(img, f"{result.names[int(box.cls[0])]}",
                            (int((box.xyxy[0][0] + box.xyxy[0][2])/2)-50, int(box.xyxy[0][1]) - 10),
                            cv2.FONT_HERSHEY_TRIPLEX, 1, (0, 255, 0), text_thickness)
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

@app.route('/api/return_item_data', methods=['GET'])
def return_item_data():
    # Print the current values for debugging
    print(f"Itemname: {itemname}, Price: {price}, Expiry: {expiry}, Info: {info}")
    
    data = {
        'itemname': itemname,   # Include itemname
        'expiry': expiry,
        'price': price,
        'info': info
    }
    return jsonify(data)


@app.route('/api/db_chart', methods=['GET'])
def return_chart_data():
    data = genchart.getitems()
    return jsonify(data)


@app.route('/')
def index_video():
    return render_template('video.html')

is_running = True
last_frame = None
last_detection = None


def gen_frames():
    global is_running, last_frame, last_detection
    cap = cv2.VideoCapture(0)
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
        frame, detections = detection.predict_and_detect(frame)

        # Save the last detected frame and detection results
        last_frame = frame
        last_detection = detections  # Save the detection results

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/stop_detection', methods=["POST"])
@cross_origin()
def stop_detection():
    global last_frame, expiry, price, info, itemname
    print("Saving the last frame...")

    # Save the last frame if it exists
    if last_frame is not None:
        image_path = os.path.join("server", "saved", "last_frame.jpg")
        cv2.imwrite(image_path, last_frame)
        print(f"Last frame saved at {image_path}")

        # Iterate over the detection results
        for result in last_detection:
            for box in result.boxes:
                class_id = int(box.cls[0])
                class_name = result.names[class_id]  # This is the item name
                print(class_name)

                # Fetch item details from the database
                resp = db.getitemclass(class_name)

                if resp:
                    itemname = resp['itemname']
                    expiry = resp['expiry']
                    price = resp['price']
                    info = resp['info']
                    
                    # Log the database result to the console
                    print(f"Database result: {resp}")
                else:
                    print("No details found for class name:", class_name)
    else:
        print("No frame to save.")

    # Return the database result to the frontend as a JSON response
    return jsonify({
        'message': "Last Frame Saved",
        'itemname': itemname,
        'expiry': expiry,
        'price': price,
        'info': info
    }), 200

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#@app.route('/last_detection')
#def get_last_detection():
#    global last_frame, last_detection, class_name
#    if last_frame is not None and last_detection is not None:
#        # Print out the last detected item
#        for result in last_detection:
#            for box in result.boxes:
#                class_id = int(box.cls[0])  # Class index
#                confidence = box.conf[0]    # Confidence score
#                class_name = result.names[class_id]  # Class name
#                print(class_name)
#                # add to database
#                db.additem(class_name, 0,0)
#                resp = tuple(db.getitemclass(class_name))
#                expiry = resp[2]
#                price = resp[3]
#
#
#        # Return the last frame as an image
#        ret, buffer = cv2.imencode('.jpg', last_frame)
#        return Response(buffer.tobytes(), mimetype='image/jpeg')
#    else:
#        return "No detection available", 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
    #http://localhost:8000/video for video source
    #http://localhost:8000 for image source
