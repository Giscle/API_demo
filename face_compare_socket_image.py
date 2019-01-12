from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import requests
g_url = 'http://socket.giscle.com'
socketio = SocketIO(g_url, 8000, LoggingNamespace)

def response(args):
    print('response', str(args['data']))

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

socketio.emit('authenticate',{'token':token})

if __name__ == "__main__":
    imgPath1 = './1.jpg'
    imgPath2 = './sample/bc2.jpeg'

    img1 = cv2.imread(imgPath1)
    img2 = cv2.imread(imgPath2)

    result, img1 = cv2.imencode('.jpg', img1)
    img1 = img1.tostring()
    img1 = base64.b64encode(img1)
    img1 = img1.decode('utf-8')

    result, img2 = cv2.imencode('.jpg', img2)
    img2 = img2.tostring()
    img2 = base64.b64encode(img2)
    img2 = img2.decode('utf-8')

    socketio.on('response', response)
    socketio.emit('Compare_face_image',  {'img1':img1,'img2':img2,'token':token,'secret':secret,'folder':'default'})
    socketio.wait(seconds=4)

    