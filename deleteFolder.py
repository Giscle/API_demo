"""
* Client side code to delete the list of images in the database.
"""
import os
import requests

token = "YOUR_API_KEY"
secret = "YOUR_SECRET_KEY"

"""
    * Use folderKey = 'default' when there is no specific folder.
    * Else use a unique folder name/key that is created.
"""
folderKey = "..."

payload = {
    'secretKey':secret,
    'apiKey':token,
    'folderKey':folderKey
}
r = requests.post('http://api.giscle.ml/face_search/delete/dir',data=payload)

if r.ok:
    print(r.json())
else:
    r.status_code
