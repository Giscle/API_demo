import requests
import base64
import cv2


token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

imgPath = "./v2.jpeg"

img = open(imgPath,'rb')
img = img.read()

img_enc = base64.b64encode(img)
img_enc = img_enc.decode('utf-8')

re = requests.post('http://api.giscle.ml/body_detection',data={'image':img_enc},headers={'token': token})

if re.ok:
    print(re.json())
    r = re.json()
    frame = cv2.imread(imgPath)
    for key in r['data'].keys():
        if key != 'total_person':
            x,y,h,w = (r['data'][str(key)])
            x,y,h,w = int(x),int(y),int(h),int(w)
            cv2.rectangle(frame, (x,y),(x+h,y+w), (255,0,0))
    while True:
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

else:
    print(r.status_code)