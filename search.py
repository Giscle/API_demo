"""
* Client side code for Face Searching API.
* Call this after adding images to the database.
"""

import requests
import cv2

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

folderKey = "default"

imageName = "dd.jpg"
img = open(imageName,'rb')

g_url = 'http://api.giscle.ml'
auth = {
    'secretKey':secret,
    'apiKey':token,
    'folderKey':folderKey
    }

r = requests.post("{}/{}".format(g_url,'face_search'),data=auth, files={'img1':img})

if r.ok:
    result = r.json()
    print(result)
    if result['label'] == 1:
        image = cv2.imread(imageName)
        for person in result['result']:
            t,r,b,l = person['face']
            cv2.rectangle(image,(l,t),(r,b),(255,255,255))
            cv2.putText(image,person['person'],(l,t-13),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
        cv2.imshow('Image',image)
        cv2.waitKey(0)

else:
    print(r.status_code)