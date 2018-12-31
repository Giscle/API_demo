
# API Tutorial

# Prerequisite

1.  Basic knowledge of Python or any programming language and Network Programming.
2.  OpenCV or any Image manipulation library
3.  Basic knowledge of Javascript Object Notation (JSON)

# Face Detection API

For authentication, only API key is required in Face Detection API and is provided as a header instead of form data. And the image is sent as base64 encoding of the file. You can find the client side code of Face Detection API written in Python3


```
import requests
import cv2
import base64

token = "YOUR_API_KEY"
g_url = 'http://api.giscle.ml'

imageName = "PATH_TO_IMAGE"
img = open(imageName,'rb')
img = img.read()
image = base64.b64encode(img)
payload = {'image':image}

r = requests.post(g_url + ':80/image', files=payload, headers={'token':token})

if r.ok:
	result = r.json()
	print(result)
	image = cv2.imread(imageName)
	for key in result['Data'][2].keys():
    	    x,y,h,w = result['Data'][2][str(key)]['rect_coordinate']
    	    cv2.rectangle(image, (x,y),(x+h,y+w), (255,255,255))
	cv2.imshow('Image',image)
	cv2.waitKey(0)
else:
	print(r.status_code)
```


When you do an HTTP Post request to Giscle server for the Face Detection API, you will find an output like this:


```
{'Data': ['frame_09a2_233e', 1, {'FACE_1c77_ee11': {'Age': 23, 'Emotion': 'sad', 'Gender': 'M', 'rect_coordinate': [52, 56, 94, 132]}}], 'Status': 'Success'}
```


The result will be a JSON object with an attribute "Data" that contains a list of all the faces, the element in the 2th position of the list is another JSON object which contains all the information about the face identified by a unique id, you can get the list of all the id using keys() method of JSON object. The "rect_coordinate" attribute give a list of numbers which are lower left coordinates of the face in the image and the next two number are the height and width of the rectangle that bounds the face.


# 


# Face Comparison API

The payload of the Face Comparison API contains the authorisation attributes and also the two images. The payload of this API looks like this:


```
payload{
    'secretKey':YOUR_SECRET_KEY,
    'apiKey':YOUR_API_KEY
}

Files{
	'img1':img1,
    'img2':img2
}
```


 You can find the client side code for this API written in Python3 below:


```
import requests
import cv2
import base64

token = YOUR_API_KEY
secret = YOUR_SECRET_KEY

g_url = 'http://api.giscle.ml'

imageName1 = "PATH_TO_IMAGE_1"
img1 = open(imageName1,'rb')
imageName2 = "PATH_TO_IMAGE_2"
img2 = open(imageName2,'rb')

files = {'img1':img1,'img2':img2}
payload = {'secretKey':secret,'apiKey':token}
r = requests.post("{}/{}".format(g_url,'face_compare'), data=payload, files=files)

if r.ok:
	result = r.json()
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
```


You can use a socket client to do this task:


### Comparing two photos


```
from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import requests
g_url = 'http://35.237.223.3:8080'
socketio = SocketIO(g_url, 5000, LoggingNamespace)


cnt=0
def response(args):
	print('response'+str(cnt), str(args['data']))


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


	# For Face Comparision
	socketio.on('response', response)
	socketio.emit('Compare_face_image',  {'img1':img1,'img2':img2,'token':token,'secret':secret,'folder':'default'})
	socketio.wait(seconds=4)
```


When you do an HTTP post request for Face Comparison API, you'll get a result like this:


```
{'status': 200, 'label': 1, 'result': [{'distance': 0.7352064619293461, 'img1': [44, 80, 151, 187], 'img2': [81, 96, 210, 225]}]}
```


The result will be a JSON data, when the attribute "label" is 0, that means the system cannot find any similarity between the two images. But if the "label" is 1, then the attribute "result" contains a list of json objects which contains and attribute "distance" which is the distance between two faces and attributes "img1" and "img2" which are the coordinates of the rectangle that bounds the face. This order of coordinates is left, top, right, bottom.


# Face Searching API

The authentication parameters of the Face Searching API is same as that of Face Comparison API.


## Adding image to database

Before you can search any photo using Face Searching API, you have to train our model using your Face Dataset, which is a directory that contains the images of all the faces with the label as the filename. For example, you want to create a software that can classify the faces of all your employees, then you have to prepare a directory of images of clear headshots of all your employes and the filename of each photo will be the employee id of corresponding face. After you prepare that director, you can write a code like this, this will read each image one by one and train our face classifying AI.


```
import os
import requests

dirpath = 'PATH_TO_DATASET_DIRECTORY'
dataset = os.listdir(dirpath)

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"
for data in dataset:
	img = open(os.path.join(dirpath,data),'rb')
	label = data.split('.')[0]

	payload = {
    	'secretKey':secret,
    	'apiKey':token,
    	'label':label,
	'folderKey':"default"
	}

	r = requests.post('http://api.giscle.ml/face_search/train',data=payload,files={'image':img})

	if r.ok:
    	print(r.json())
```



## Get the dataset

Then you can verify that all the images are trained by using the "**dataset**" functionality of Face Searching API, you can write a code similar to this:


```
import os
import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

payload = {
	'secretKey':secret,
	'apiKey':token,
	'folderKey':"default"
}
r = requests.post('http://api.giscle.ml/face_search/dataset',data=payload)

if r.ok:
	result = r.json()
	for key in result.keys():
    	print(result[key]['label'])
else:
```


**<code>	r.status_code</code></strong> 


## Search Faces

After training the dataset, you can search or recognize a particular face. The authentication payload is same as Face Detection API, but this time, you have to send the raw image binary instead of base64 encoding or raw character encoding of the image. You can write a client side code similar to this:


```
import requests
import cv2

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

imageName = "rd1.jpg"
img = open(imageName,'rb')

g_url = 'http://api.giscle.ml'
auth = {
	'secretKey':secret,
	'apiKey':token,
	'folderKey':"default"
	}

r = requests.post("{}/{}".format(g_url,'face_search'),data=auth, files={'img1':img})

if r.ok:
	result = r.json()
	if result['label'] == 1:
    	image = cv2.imread(imageName)
    	for person in result['result']:
        	    t,r,b,l = person['face']
        	    cv2.rectangle(image,(l,t),(r,b),(255,255,255))          cv2.putText(image,person['person'],(l,t-13),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255))
    	cv2.imshow('Image',image)
    	cv2.waitKey(0)

else:
	print(r.status_code)
```


You can search using a Socket client like this:


### Searching a photo


```
from socketIO_client import SocketIO, LoggingNamespace
import cv2
import hashlib
import base64
import requests
g_url = 'http://35.237.223.3:8080'
socketio = SocketIO(g_url, 5000, LoggingNamespace)


def response(args):
	print('response'+str(cnt), str(args['data']))


socketio.emit('authenticate',{'token':token})


if __name__ == "__main__":
	imgPath1 = '...'


	img1 = cv2.imread(imgPath1)


	result, img1 = cv2.imencode('.jpg', img1)
	img1 = img1.tostring()
	img1 = base64.b64encode(img1)
	img1 = img1.decode('utf-8')


	# For face search
	socketio.on('response', response)
	socketio.emit('Search_face',  {'img1':img1,'token':token,'secret':secret,'folder':'default'})
	socketio.wait(seconds=4)
```



### Searching a face in a video

(Authentication of the socket is same as that of searching in photo)


```
vidPath = '...'
vidcap = cv2.VideoCapture(vidPath)
success, img1 = vidcap.read()
success = True
while success:
    	result, img1 = cv2.imencode('.jpg', img1)
    	img1 = base64.b64encode(img1)
    	img1 = img1.decode('utf-8')
    	socketio.emit('Search_face', {'img1': img1, 'token':token,'secret':secret,'folder':'default'})
    	socketio.wait(seconds=4)
    	print("sending")
    	success, img1 = vidcap.read()
```

When you do a HTTP post request to Face Searching API, which is same as Face Recognition API, you will get a result like this:


```
{'label': 1, 'result': [{'face': [268, 483, 397, 354], 'person': 'Benedict Cumberbatch'}]}
```

The attribute "label" in the JSON object which you get as a result, signifies whether there is a match or not. If the label is 1, then the attribute "result" will contain a list of JSON objects which has two attributes: "face" this is a list of rectangle coordinates ordered as Top-Right and Bottom- Left corner coordinates of the rectangle that bounds the face and "person" which specifies the corresponding label of that person that you mentioned as the filename while training the dataset.

## Delete Dataset
This API also provides an option to truncate all your photos, you can use that functionality using a client side code similar to this.
```
import os
import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

payload = {
	'secretKey':secret,
	'apiKey':token
}
r = requests.post('http://api.giscle.ml/face_search/delete',data=payload)

if r.ok:
	print(r.json())
else:
	R.status_code
```

## Delete Folder
Change the request to this, if you want to delete the folder along with all the images in it.
```
payload = {
	'secretKey':secret,
	'apiKey':token,
	'folderKey':folderKey
}
r = requests.post('http://api.giscle.ml/face_search/delete/dir',data=payload)
```

## Delete a single image
And finally, if you want to delete a particular image then this.
```
payload = {
	'secretKey':secret,
	'apiKey':token,
	'folderKey':folderKey,
	'imageKey':imgId
}

r = requests.post('http://api.giscle.ml/face_search/delete/image',data=payload)
```

# Errors
*   Whenever you mention the authentication parameters wrong or invalid, then a status 400 will be initiated from the server.
*   You will also find 400 status code, when you miss one of the required payload attribute or used wrong payload label other than that used above codes.
*   An error code of 405 will be initiated if you are doing a GET request instead of POST request
*   And error code 500 means there is something wrong with the image file, like a corrupted file or used a file that is not an image file or an image file that is compressed using uncommon/unconventional compression algorithms.