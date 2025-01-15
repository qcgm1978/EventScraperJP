from bs4 import BeautifulSoup
import requests
import re

url = "https://t.pia.jp/pia/event/event.do?eventBundleCd=b2452501"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")

# tags = doc.find_all(text=re.compile("2025.*"), limit=1)
# for tag in tags:
#     print(tag.strip())