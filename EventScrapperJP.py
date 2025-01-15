import requests
from bs4 import BeautifulSoup
import openpyxl

url = "https://t.pia.jp/music/"
pagePia = requests.get(url)
pagePia.encoding = 'utf-8'
html_content_Pia = pagePia.text


doc_Pia = BeautifulSoup(html_content_Pia, "html.parser")

concerts = []

for div_Pia in doc_Pia.find_all("div"):
    
    a_tag_Pia = div_Pia.find("a")
    if a_tag_Pia:
        
        figcaption_Pia = a_tag_Pia.find("figcaption")
        
        if figcaption_Pia:
            
            name_concert_Pia = figcaption_Pia.find("h2")
            namePia = name_concert_Pia.get_text(strip=True) if name_concert_Pia else None
            
            date_concert_Pia= figcaption_Pia.find("span")
            datePia = date_concert_Pia.get_text(strip=True) if date_concert_Pia else None
            
            linkPia = a_tag_Pia.get("href") if a_tag_Pia else None
            
            if namePia and datePia and linkPia:
                if not any(linkPia in concert["Link"] for concert in concerts):
                    concerts.append({"Name": namePia, "Date": datePia, "Link": linkPia})

excel_file = "concerts.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "ConcertsPia"
sheet.append(["Name", "Date", "Link"])

for concert in concerts:
    sheet.append([concert["Name"], concert["Date"], concert["Link"]])
workbook.save(excel_file)

print(f"Scraped {len(concerts)} concerts. Data saved to {excel_file}.")