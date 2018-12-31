"""
* Client side code for add images to the database.
"""
import os
import requests

dirpath = './dataset'
dataset = os.listdir(dirpath)

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

"""
    * Use folderKey = 'default' when there is no specific folder.
    * Else use a unique folder name/key that is created.
"""
folderKey = "default"

for data in dataset:
    img = open(os.path.join(dirpath,data),'rb')
    label = data.split('.')[0]

    payload = {
        'secretKey':secret,
        'apiKey':token,
        'label':label,
        'folderKey':folderKey
    }

    r = requests.post('http://api.giscle.ml/face_search/train',data=payload,files={'image':img})

    if r.ok:
        print(r.json())
