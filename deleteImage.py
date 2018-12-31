import os
import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

"""
   * You'll get the image id (imgId) from getDataset API
"""
imgId = '...'

"""
    * Use folderKey = 'default' when there is no specific folder.
    * Else use a unique folder name/key that is created.
"""
folderKey = '...'

payload = {
    'secretKey':secret,
    'apiKey':token,
    'folderKey':folderKey,
    'imageKey':imgId
}

r = requests.post('http://api.giscle.ml/face_search/delete/image',data=payload)

if r.ok:
    print(r.json())
else:
    print(r.status_code)
