import cv2
import hashlib
import base64
import requests
import json
import numpy as np
from socketIO_client import SocketIO, LoggingNamespace
frame= np.random.randint(255, size=(900,800,3),dtype=np.uint8)

socketio = SocketIO('http://socket.giscle.com', 5000, LoggingNamespace)
blinkingDetect=0
def response(args):
    result = json.loads(json.dumps(args['data']))
    result = json.loads(result)
    print(result)
    global blinkingDetect
    global frame

    for i in result['Result']:
        leftEyeHull=i['leftEyeHull']
        rightEyeHull=i['rightEyeHull']
        blinking=i['Blinking']
        print(leftEyeHull)
        cv2.drawContours(frame, [np.asarray(leftEyeHull)], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [np.asarray(rightEyeHull)], -1, (0, 255, 0), 1)
        if blinking ==1:
            blinkingDetect += 1
            
def eye_blinking_video():
    vidcap = cv2.VideoCapture(0)
    global frame
    while True:
        success, img2 = vidcap.read()
        frame = img2.copy()
        result, img2 = cv2.imencode('.jpg', img2)
        img2 = img2.tostring()
        img2 = base64.b64encode(img2)
        img2 = img2.decode('utf-8')
        print("sending frames to Eye blinking")
        socketio.emit('Eye_Blinking', { 'img': img2})
        socketio.wait(seconds=0.3)
        frame = cv2.resize(frame, (900, 600))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(blinkingDetect)
            vidcap.release()
            cv2.destroyAllWindows()
            break
        if blinkingDetect == 3:
            vidcap.release()
            cv2.destroyAllWindows()
            send_Video_face_search()
            break
    
socketio2 = SocketIO('http://socket.giscle.com', 8000, LoggingNamespace)

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"
folder = "default"
def response2(args):
    print('response', str(args['data']))
    
def send_Video_face_search():
    vidcap = cv2.VideoCapture(0)
    success, img2 = vidcap.read()
    success = True
    while success:
        result, img2 = cv2.imencode('.jpg', img2)
        img2 = img2.tostring()
        img2 = base64.b64encode(img2)
        img2 = img2.decode('utf-8')
        print("sending frames to face searching")
        socketio2.emit('Search_face',  {'img1':img2,'token':token,'secret':secret,'folder':folder})
        socketio2.wait(seconds=2)
        success, img2 = vidcap.read()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    socketio2.on('response', response2)
    socketio.on('response', response)
    eye_blinking_video()

