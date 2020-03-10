import sqlite3
import cv2
import os
import numpy as np
import datetime
import sys
import picamera
import io
from flask import Flask, send_file, Response
import threading

app = Flask(__name__)

def read():
    data = io.BytesIO()
    with picamera.PiCamera() as camera:
            camera.capture(data, format='jpeg')
    data = np.fromstring(data.getvalue(), dtype=np.uint8)
    image = cv2.imdecode(data, 1)
    return image

def recognize():
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath) 
    while(True): 
        frame = read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face = faceCascade.detectMultiScale(gray, 1.2,5)
        for (x,y,w,h) in face:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(225,0,0),2)
        is_success, im_buf_arr = cv2.imencode(".jpg", frame)
        byte_im = im_buf_arr.tobytes()
        yield(bR'--frame\r\nContent-Type:image/jpeg\r\n\r\r'+frame+bR'\r\n')

@app.route("/start")
def start():
	"""
	task = threading.Thread(target=recognize)
	task.daemon = True
	task.start()
	"""
	return Response(recognize(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/show")
def show():
	return send_file("output.jpg")

if __name__ == "__main__":
	app.run(host="0.0.0.0", port="8000")
