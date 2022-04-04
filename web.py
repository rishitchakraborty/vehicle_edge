#Import necessary libraries
import time
from flask import Flask, render_template, Response
import os
import multipleVideo
import detect as yolo
#Initialize the Flask app
app = Flask(__name__)
import cv2
import random

import os
import boto3

# Create Session
session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key='',
)
# Initiate S3 Resource
s3 = session.resource('s3')
# Select Your S3 Bucket
your_bucket = s3.Bucket('rishit-lambda')
for s3_object in your_bucket.objects.all():
    #your_bucket.download_file(s3_object.key, filename_with_extension)
    path, filename = os.path.split(s3_object.key)
    #os.makedirs(path)
    PATH ="RECORDS"
    filename2= "./RECORDS/" + filename
    your_bucket.download_file(s3_object.key, filename2)
    print("Downloading Done")

time.sleep(15)
camera = cv2.VideoCapture('test2.avi')

'''
for ip camera use - rtsp://username:password@ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp'
for local webcam use cv2.VideoCapture(0)


def gen_frames():
    while True:
        success, frame = camera.read()  # read the camera frame
        #ret, buffer=yolo.run(source=frame)
        ret, buffer = cv2.imencode('.jpg', frame)

        if not success:
            break
        else:
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
'''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    L1 = []
    for items in multipleVideo.multipleVideoPlayingFunction("RECORD"):
        print(items)
        L1.append(items)

    def controller(parse, list_par):
        if parse:
            return random.randint(0, len(list_par)-1)
        else:
            pass

    return Response(yolo.run(source=L1[controller(True, L1)], view_img=True),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":

    for _ in range(len(os.listdir("RECORD"))):

        app.run(host='0.0.0.0',port=8080,debug=False)



