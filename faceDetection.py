import requests
import cv2
import base64

token = "YOUR_API_KEY"

g_url = 'http://api.giscle.ml'

imageName = "..."
img = open(imageName,'rb')
img = img.read()
image = base64.b64encode(img)
payload = {'image':image}

r = requests.post(g_url + ':80/image', files=payload, headers={'token':token,'store':str(0)})

if r.ok:
    result = r.json()
    print(result)
    image = cv2.imread(imageName)
    for key in result['Data'][2].keys():
        x,y,h,w = result['Data'][2][str(key)]['rect_coordinate']
        cv2.rectangle(image, (x,y),(x+h,y+w), (255,255,255))
        text = "Emotion: "+result['Data'][2][str(key)]['Emotion']
        text = "Age:"+str(result['Data'][2][str(key)]['Age'])+", Gender:"+result['Data'][2][str(key)]['Gender']
        cv2.putText(image,text,(x,y-13),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
    cv2.imshow('Image',image)
    cv2.waitKey(0)
else:
    print(r.status_code)
