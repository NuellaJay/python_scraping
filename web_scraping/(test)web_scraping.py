import requests
from bs4 import BeautifulSoup as bs

search = input("What are you looking for? ")
url = "https://explainshell.com/explain?cmd=" + search
page = requests.get(url)
soup = bs(page.text, "lxml")
exp = soup.find_all("pre",class_="help-box")
for each in exp:
    print(each)

