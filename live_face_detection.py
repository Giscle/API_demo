from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import time

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFwdXJ2LmNoYXVkaGFyeTA2QGdtYWlsLmNvbSIsInVzZXJuYW1lIjoiYXB1cnYwNiIsImZpcnN0bmFtZSI6IkFwdXJ2In0.ogOgdOo4NQjQlJbxtvmvwD2f2ns7guDIIoHYlyfxOMo"

g_url = 'http://api.giscle.ml'

frame = 0

def extract_data(args):
    print(args)

    font = cv2.FONT_HERSHEY_SIMPLEX
    for key in args['Output'][2].keys():
        x,y,h,w = args['Output'][2][str(key)]['rect_coordinate']
        cv2.rectangle(frame, (x,y),(x+h,y+w), (255,255,255))
        cv2.imshow("frame",frame)



socketio = SocketIO(g_url, 80, LoggingNamespace)

socketio.emit('authenticate', {'token': token})

cam = cv2.VideoCapture(0)

frame_count = 1

while True:
    global t
    t = time.time()
    ret, frame = cam.read()
    if not ret:
        continue
    frame = cv2.resize(frame, (900, 600))
    encoded, buffer = cv2.imencode('.jpg', frame)
    encoded_frame = base64.b64encode(buffer)
    encoded_frame = encoded_frame.decode('utf-8')
    socketio.emit('faged', {'data': encoded_frame,'store':0})
    socketio.on('response', extract_data)
    socketio.wait(0.1)
    print(time.time() - t)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

socketio.disconnect()
cam.release()
