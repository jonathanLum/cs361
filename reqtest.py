import requests
from requests.structures import CaseInsensitiveDict

url = "https://graph-microservice.herokuapp.com/"

headers = CaseInsensitiveDict()
headers["Content-Type"] = "application/json"

data = """
{"filename": "newimage2",
"dpi": 300,
"format": "line",
"output": "PNG",
"filename": "graph",
"title": "Test Graph",
"xlabel": "X",
"ylabel": "Y",
"legend": true,
"grid": false,
"entries": [[[1,2,3,4,5], [7,4,2,8,9], "r", "line1"], 
            [[2,5,7,8,9], [-10,2,5,9,-3], "b", "line2"]]}
"""


r = requests.post(url, headers=headers, data=data)
print(r)
print(r.headers)

name = "img.png"
with open(name, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)

