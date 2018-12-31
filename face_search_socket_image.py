from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import requests
g_url = 'http://35.237.223.3'
socketio = SocketIO(g_url, 5000, LoggingNamespace)

def response(args):
    print('response', str(args))

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

socketio.emit('authenticate',{'token':token})

if __name__ == "__main__":
    imgPath1 = './1.jpg'
    img1 = cv2.imread(imgPath1)

    result, img1 = cv2.imencode('.jpg', img1)
    img1 = img1.tostring()
    img1 = base64.b64encode(img1)
    img1 = img1.decode('utf-8')

    socketio.on('response', response)
    socketio.emit('Search_face',  {'img1':img1,'token':token,'secret':secret,'folder':'default'})
    socketio.wait(seconds=4)