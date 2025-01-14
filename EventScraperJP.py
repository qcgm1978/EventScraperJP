from bs4 import BeautifulSoup
import requests

page_to_scrape = requests.get("https://t.pia.jp")