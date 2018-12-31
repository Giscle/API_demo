import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

"""
    * Use folderKey = 'default' when there is no specific folder.
    * Else use a unique folder name/key that is created.
"""
folderKey = "default"

imgPath = "dd.jpg"
label = "Diksha Bajaj"

img = open(imgPath,'rb')

payload = {
    'secretKey':secret,
    'apiKey':token,
    'label':label,
    'folderKey':folderKey
}

r = requests.post('http://api.giscle.ml/face_search/train',data=payload,files={'image':img})

if r.ok:
    print(r.json())
else:
    print(r.status_code)