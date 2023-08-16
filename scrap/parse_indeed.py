from bs4 import BeautifulSoup

with open("./indeed_local.htm", "r", encoding="utf-8") as file:
    html_content = file.read()

soup = BeautifulSoup(html_content, "html.parser")
jobs_container = soup.select_one(".jobsearch-ResultsList")
jobs_list = jobs_container.findAll("li")
i = 0

for jobs in jobs_list:
    i = i + 1
print(i)
