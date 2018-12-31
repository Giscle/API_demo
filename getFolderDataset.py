"""
* Client side code to get the list of images in the database.
"""
import os
import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

folderKey = "default"

payload = {
    'secretKey':secret,
    'apiKey':token,
}
r = requests.post('http://api.giscle.ml/face_search/dataset',data=payload)

if r.ok:
    result = r.json()
    if (result):
        for key in result[folderKey].keys():
            print("id:",key,",folder:",folderKey,",label:",result[folderKey][key]['label'])
else:
    r.status_code