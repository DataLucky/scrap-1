import json

import requests
from config import API_BASE_URL

response = requests.get(f"{API_BASE_URL}/indeed")
if response.ok:
    response_json = json.dumps(response.json())
    with open("lang_pop.json", "w") as file:
        file.write(response_json)
