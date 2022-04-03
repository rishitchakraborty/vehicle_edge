from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
from threading import Thread
import multipleVideo
import imutils
from moviepy.editor import *

global capture,rec_frame, grey, switch, neg, face, rec, out 
capture=0
grey=0
neg=0
face=0
switch=0
rec=0



#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

video_list = multipleVideo.multipleVideoPlayingFunction('RECORDS')
frame_list = []
print(video_list)

for items in video_list:

    camera = cv2.VideoCapture(items)
    counter = 1


    def gen_frames():  # generate frame by frame from camera
        global out, capture,rec_frame
        frame_list = []
        counter = 1
        while True:
            success, frame = camera.read()
            frame_list.append(frame)
            counter += 1
            flip = cv2.flip(frame, 4)
            frame = flip
            # frame = imutils.resize(frame, width=320)
            if success:

                if(grey):
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                if(neg):
                    frame=cv2.bitwise_not(frame)

                try:
                    ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                except Exception as e:
                    pass

            else:
                pass
            if cv2.waitKey(60) & counter == len(frame_list):
                break

        # vidCapture.release()
        # cv2.destroyAllWindows()

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route('/video_feed')
    def video_feed():
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

    @app.route('/requests',methods=['POST','GET'])
    def tasks():
        global switch,camera
        if request.method == 'POST':
            if request.form.get('click') == 'Capture':
                global capture
                capture=1

        elif request.method=='GET':
            return render_template('index.html')
        return render_template('index.html')


    if __name__ == '__main__':
        app.run()
        
    # camera.release()
    # cv2.destroyAllWindows()     