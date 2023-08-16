import json

import requests

base_url = "https://api.stackexchange.com/2.2"
questions = base_url + "/questions?site=stackoverflow&pagesize=50"

response = requests.get(questions)


if response.ok:
    with open("indeed.html", "w") as file:
        file.write(response.text)
