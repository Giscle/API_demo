import os
import requests

masterDirPath = "./masterDS"

subDirs = os.listdir(masterDirPath)

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

"""
    * Use folderKey = 'default' when there is no specific folder.
    * Else use a unique folder name/key that is created.
"""
folderKey = "..."

for label in subDirs:
    subDirPath = os.path.join(masterDirPath,label)
    images = os.listdir(subDirPath)
    for image in images:
        img = open(os.path.join(subDirPath,image),'rb')
        payload = {
            'secretKey':secret,
            'apiKey':token,
            'label':label,
            'folderKey':folderKey
        }
        r = requests.post('http://api.giscle.ml/face_search/train',data=payload,files={'image':img})
        if r.ok:
            print(r.json())
