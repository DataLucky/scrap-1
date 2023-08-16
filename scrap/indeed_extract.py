import json

import requests

response = requests.get(
    "https://api.scrapingdog.com/scrape?api_key=64db7319ca8e8153dd8be311&url=https://www.indeed.com/jobs?q=developer&dynamic=false"
)
if response.ok:
    with open("indeed2.html", "w") as f:
        f.write(response.text)
