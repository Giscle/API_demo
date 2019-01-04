from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import requests
g_url = 'http://35.237.223.3'
socketio = SocketIO(g_url, 5000, LoggingNamespace)

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

socketio.emit('authenticate',{'token':token})

def response(args):
    print('response', str(args['data']))

def send_Video_face_compare():
    imgPath1 = '...'
    vidPath = '...'
    img1 = open(imgPath1, "rb").read()
    img1 = base64.b64encode(img1)
    img1 = img1.decode('utf-8')
    vidcap = cv2.VideoCapture(vidPath)
    success, img2 = vidcap.read()
    success = True
    while success:
        result, img2 = cv2.imencode('.jpg', img2)
        img2 = img2.tostring()
        img2 = base64.b64encode(img2)
        img2 = img2.decode('utf-8')
        socketio.emit('Compare_face_image', {'img1': img1, 'img2': img2, 'token':token,'secret':secret})
        socketio.wait(seconds=2)
        print("sending")
        success, img2 = vidcap.read()

if __name__ == "__main__":
    send_Video_face_search()