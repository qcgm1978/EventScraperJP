from bs4 import BeautifulSoup
import requests

with open("dummy.html", "r") as f:
    doc = BeautifulSoup(f, "html.parser")
    
print(doc)