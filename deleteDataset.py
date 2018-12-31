"""
* Client side code to delete the list of images in the database.
"""
import os
import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

payload = {
    'secretKey':secret,
    'apiKey':token,
}
r = requests.post('http://api.giscle.ml/face_search/delete',data=payload)

if r.ok:
    print(r.json())
else:
    r.status_code
