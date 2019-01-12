from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import requests

socketio = SocketIO('http://socket.giscle.com', 8000, LoggingNamespace)

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"
folder = "..."

def response(args):
    print('response', str(args['data']))

def send_Video_face_search():
    vidcap = cv2.VideoCapture('./ddd.mp4')
    success, img2 = vidcap.read()
    success = True
    while success:
        result, img2 = cv2.imencode('.jpg', img2)
        img2 = img2.tostring()
        img2 = base64.b64encode(img2)
        img2 = img2.decode('utf-8')
        print("sending")
        socketio.emit('Search_face',  {'img1':img2,'token':token,'secret':secret,'folder':folder})
        socketio.wait(seconds=2)
        success, img2 = vidcap.read()


if __name__ == "__main__":
    socketio.emit('authenticate',{'token':token})
    socketio.on('response', response)
    send_Video_face_search()
