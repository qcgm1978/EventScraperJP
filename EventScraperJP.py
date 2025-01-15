from bs4 import BeautifulSoup
import requests

with open("dummy.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")
    
tags = doc.find_all("p")[0]

print(tags.find_all("b"))