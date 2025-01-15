import requests
from bs4 import BeautifulSoup
import openpyxl
import pykakasi
import pandas as pd

url = "https://t.pia.jp/music/"
pagePiaC = requests.get(url)
pagePiaC.encoding = 'utf-8'
html_content_PiaC = pagePiaC.text


doc_PiaC = BeautifulSoup(html_content_PiaC, "html.parser")

url2 = "https://t.pia.jp/anime/"
pagePiaA = requests.get(url2)
pagePiaA.encoding = 'utf-8'
html_content_PiaA = pagePiaA.text


doc_PiaA = BeautifulSoup(html_content_PiaA, "html.parser")

url3 = "https://t.pia.jp/event/"
pagePiaE = requests.get(url3)
pagePiaE.encoding = 'utf-8'
html_content_PiaE = pagePiaE.text


doc_PiaE = BeautifulSoup(html_content_PiaA, "html.parser")

def convert_to_romaji(japanese_text):
    kks = pykakasi.kakasi()
    result = kks.convert(japanese_text)
    romaji_text = ''.join([item['hepburn'] for item in result])
    return romaji_text

def PiaScrapper(doc_Pia):
    concerts = []
    for div_Pia in doc_Pia.find_all("div"):
        
        a_tag_Pia = div_Pia.find("a")
        if a_tag_Pia:
            
            figcaption_Pia = a_tag_Pia.find("figcaption")
            
            if figcaption_Pia:
                
                name_concert_Pia = figcaption_Pia.find("h2")
                namePia = name_concert_Pia.get_text(strip=True) if name_concert_Pia else None
                
                if namePia:
                    RomajiPia = convert_to_romaji(namePia)
                else:
                    RomajiPia = None
                    
                date_concert_Pia= figcaption_Pia.find("span")
                datePia = date_concert_Pia.get_text(strip=True) if date_concert_Pia else None
                
                linkPia = a_tag_Pia.get("href") if a_tag_Pia else None
                
                if namePia and datePia and linkPia:
                    if not any(linkPia in concert["Link"] for concert in concerts):
                        concerts.append({"Name": namePia, "Romaji": RomajiPia, "Date": datePia, "Link": linkPia})
    return concerts

concerts = PiaScrapper(doc_PiaC) + PiaScrapper(doc_PiaA) + PiaScrapper(doc_PiaE)

excel_file = "Events.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "EventsJP2025"
sheet.append(["Name", "Romaji", "Date", "Link"])

for concert in concerts:
    sheet.append([concert["Name"], concert["Romaji"], concert["Date"], concert["Link"]])

workbook.save(excel_file)

def remove_duplicates_in_excel(file_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    unique_rows = [headers]

    seen = set()
    for row in rows[1:]:
        link = row[3] #Change if columns moved
        if link not in seen:
            unique_rows.append(row)
            seen.add(link)

    sheet.delete_rows(1, sheet.max_row)
    for unique_row in unique_rows:
        sheet.append(unique_row)

    workbook.save(file_name)

remove_duplicates_in_excel(excel_file)

print(f"Scraped {len(concerts)} concerts. Data saved to {excel_file}.")