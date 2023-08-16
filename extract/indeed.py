import json

import requests
from config import API_BASE_URL

response = requests.get(f"{API_BASE_URL}/indeed")
if response.ok:
    with open("../data/indeed.json", "w") as f:
        f.write(json.dumps(response.json()))
