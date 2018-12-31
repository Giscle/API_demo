"""
* Client side code to get the list of images in the database.
"""
import os
import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

payload = {
    'secretKey':secret,
    'apiKey':token,
}
r = requests.post('http://api.giscle.ml/face_search/dataset',data=payload)

if r.ok:
    result = r.json()
    print(result)
    # if (result):
    #     for folder in result.keys():
    #         for key in result[folder].keys():
    #             print("id:",key,",folder:",folder,",label:",result[folder][key]['label'])
else:
    r.status_code