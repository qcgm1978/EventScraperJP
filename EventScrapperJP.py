import requests
import re
from bs4 import BeautifulSoup
import openpyxl
import pykakasi
import pandas as pd

def doc_Pia_from_url(url):
    pagePia = requests.get(url)
    pagePia.encoding = 'utf-8'
    html_content_Pia = pagePia.text
    doc_Pia = BeautifulSoup(html_content_Pia, "html.parser")
    return doc_Pia

doc_PiaM = doc_Pia_from_url("https://t.pia.jp/music/")
doc_PiaA = doc_Pia_from_url("https://t.pia.jp/anime/")
doc_PiaE = doc_Pia_from_url("https://t.pia.jp/event/")

def convert_to_romaji(japanese_text):
    kks = pykakasi.kakasi()
    result = kks.convert(japanese_text)
    romaji_text = ''.join([item['hepburn'] for item in result])
    return romaji_text

def PiaInnerScrapper(url):
    Inner_doc_Pia = doc_Pia_from_url(url)
    PPia = Inner_doc_Pia.find(string=re.compile("会場.*"))
    return convert_to_romaji(PPia)
     

def PiaScrapper(doc_Pia):
    i=0
    concerts = []
    for div_Pia in doc_Pia.find_all("div"):
        
        a_tag_Pia = div_Pia.find("a")
        if a_tag_Pia:
            
            figcaption_Pia = a_tag_Pia.find("figcaption")
            
            if figcaption_Pia:
                
                name_Pia = figcaption_Pia.find("h2")
                namePia = name_Pia.get_text(strip=True) if name_Pia else None
                
                if namePia:
                    romajiPia = convert_to_romaji(namePia)
                else:
                    romajiPia = None
                    
                date_Pia= figcaption_Pia.find("span")
                datePia = date_Pia.get_text(strip=True) if date_Pia else None
                
                linkPia = a_tag_Pia.get("href") if a_tag_Pia else None
                               
                placePia = PiaInnerScrapper(linkPia)
                                 
                if namePia and datePia and linkPia:
                    if not any(linkPia in concert["Link"] for concert in concerts):
                        concerts.append({"Name": namePia, "Romaji": romajiPia, "Place": placePia, "Date": datePia, "Link": linkPia})
                        i+=1
                        print(i)                       
    return concerts

concerts = PiaScrapper(doc_PiaM) + PiaScrapper(doc_PiaA) + PiaScrapper(doc_PiaE)

excel_file = "Events.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "EventsJP2025"
sheet.append(["Name", "Romaji", "Place", "Date", "Link"]) #If new column added, change.

for concert in concerts:
    sheet.append([concert["Name"], concert["Romaji"], concert["Place"], concert["Date"], concert["Link"]])

workbook.save(excel_file)

def remove_duplicates_in_excel(file_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    rows = list(sheet.iter_rows(values_only=True))
    headers = rows[0]
    unique_rows = [headers]

    seen = set()
    for row in rows[1:]:
        link = row[4] #Change if columns moved
        if link not in seen:
            unique_rows.append(row)
            seen.add(link)

    sheet.delete_rows(1, sheet.max_row)
    for unique_row in unique_rows:
        sheet.append(unique_row)

    workbook.save(file_name)
remove_duplicates_in_excel(excel_file)

print(f"Scraped {len(concerts)} concerts. Data saved to {excel_file}.")