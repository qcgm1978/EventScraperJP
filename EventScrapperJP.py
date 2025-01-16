import requests
import re
from bs4 import BeautifulSoup
import openpyxl
import pykakasi
import pandas as pd
import time
from openpyxl.styles import Font, Color, PatternFill, Alignment, Fill
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter

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
    for div_Inner_Pia in Inner_doc_Pia.find_all("div", class_="textDefinitionList-2024__item"):
        dt_tag_Pia = div_Inner_Pia.find("dt", class_="textDefinitionList-2024__title")
        if dt_tag_Pia and "会場" in dt_tag_Pia.get_text(strip=True):
            dd_tag_Pia = div_Inner_Pia.find("dd", class_="textDefinitionList-2024__desc")
            if dd_tag_Pia:
                return dd_tag_Pia.get_text(strip=True)
                #if PPia:
                #    return convert_to_romaji(PPia)
                #else:
                #    return None   

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
                        #if i>1:
                        #    break #tester
                        print(i)                       
    print(f"Finished scraping current site. Proceeding to the next one.")
    return concerts

concerts = PiaScrapper(doc_PiaM) + PiaScrapper(doc_PiaA) + PiaScrapper(doc_PiaE)

excel_file = "Events.xlsx"
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet.title = "EventsJP2025"
sheet.append(["Name", "Romaji", "Place", "Date", "Link"]) #If new column added, change.

for concert in concerts:
    sheet.append([concert["Name"], concert["Romaji"], concert["Place"], concert["Date"], concert["Link"]])
try:
    workbook.save(excel_file)
except: 
    print("Zamknij Excela debilu")
    time.sleep(10)
    workbook.save(excel_file)

def remove_duplicates_in_excel_pia(file_name):
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
    
remove_duplicates_in_excel_pia(excel_file)

def style_sort_excel_pia(file_name):
    workbook = openpyxl.load_workbook(file_name)
    sheet = workbook.active
    row_count = sheet.max_row
    column_count = sheet.max_column
    
    df = pd.DataFrame(sheet.values)
    headers = df.iloc[0]
    df = df[1:]
    df.columns = headers
    df = df.sort_values(by="Date", ascending=True)
    sheet.delete_rows(1, sheet.max_row)
    for row in [df.columns.tolist()] + df.values.tolist():
       sheet.append(row)
    
    title_row_style = Font(size=14, color="FFFFFF", bold=True)
    for i in range (0,column_count):
        sheet.cell(row=1, column=i+1).font = title_row_style
    dim_holder = DimensionHolder(worksheet=sheet)
    for col in range(sheet.min_column, sheet.max_column + 1):
        dim_holder[get_column_letter(col)] = ColumnDimension(sheet, min=col, max=col, width=35)
    sheet.column_dimensions = dim_holder
    
    for z in range (0, column_count):
        sheet.cell(row=1, column = z + 1).fill = PatternFill(start_color="38AA49", end_color="38AA49", fill_type="solid")
    for x in range(2, row_count):
        for z in range (0, column_count): 
            c = sheet.cell(row=x, column=z + 1)
            if x % 2 != 0:
                c.fill = PatternFill(start_color="ACFFB8", end_color="ACFFB8", fill_type="solid")
    if row_count % 2 != 0:
        for z in range (0, column_count):
            l = sheet.cell(row=row_count, column=z + 1)
            l.fill = PatternFill(start_color="ACFFB8", end_color="ACFFB8", fill_type="solid")
    
    workbook.save(file_name)
    
style_sort_excel_pia(excel_file)
print(f"Done! Scraped {len(concerts)} events. Data saved to {excel_file}.")