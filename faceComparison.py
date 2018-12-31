import requests
import cv2
import base64

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

g_url = 'http://api.giscle.ml'

imageName1 = "dd.jpg"
img1 = open(imageName1,'rb')
imageName2 = "dd.jpg"
img2 = open(imageName2,'rb')

payload = {'secretKey':secret,'apiKey':token}
files = {'img1':img1,'img2':img2}
r = requests.post("{}/{}".format(g_url,'face_compare'), data=payload,files=files)

if r.ok:
    result = r.json()
    print(result)
    if result['label'] == 1:
        image1 = cv2.imread(imageName1)
        image2 = cv2.imread(imageName2)
        for r in result['result']:
            l1,t1,r1,b1 = r['img1']
            cv2.rectangle(image1, (l1,t1),(r1,b1), (255,255,255))
            l2,t2,r2,b2 = r['img2']
            cv2.rectangle(image2, (l2,t2),(r2,b2), (255,255,255))
        cv2.imshow('Image1',image1)
        cv2.imshow('Image2',image2)
        cv2.waitKey(0)
else:
    print(r.status_code)