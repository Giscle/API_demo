import requests
import cv2
import base64
import time
import numpy as np
from PIL import Image

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

g_url = 'http://api.giscle.ml'
folderKey = "FaceDetection"

def faceDetection(img):
    img = img.read()
    image = base64.b64encode(img)
    payload = {'image':image}
    r = requests.post(g_url + ':80/image', files=payload, headers={'token':token})
    if r.ok:
        return r.json()

def faceSearching(img):
    auth = {
    'secretKey':secret,
    'apiKey':token,
    'folderKey':folderKey
    }
    r = requests.post("{}/{}".format(g_url,'face_search'),data=auth, files={'img1':img})
    if r.ok:
        return r.json()

def faceTrain(face,label):
    payload = {
    'secretKey':secret,
    'apiKey':token,
    'label':label,
    'folderKey':folderKey
    }
    r = requests.post('http://api.giscle.ml/face_search/train',data=payload,files={'image':img})
    if r.ok:
        return r.json()

def getFace(img, rect):
    x,y,w,h = rect
    img = img[y:y+h,x:x+w]

    while(True):
        cv2.imshow("frame",img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return np.array(img)


if __name__ == "__main__":

    imPath = 'temp.png'

    img = open(imPath,'rb')
    rd = faceDetection(img)
    img.seek(0)
    rs = faceSearching(img)
    img.seek(0)

    if(rs['label'] == 1):
        print(rs)
    else:
        for key in rd['Data'][2].keys():
            label = key
            face =  getFace(cv2.imread(imPath),rd['Data'][2][key]['rect_coordinate'])
            print(faceTrain(face,label))