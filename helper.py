import requests
import re
from bs4 import BeautifulSoup
import openpyxl
import pykakasi
import pandas as pd
import time
import os
from openpyxl.styles import Font, Color, PatternFill, Alignment, Fill
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter
EXCEL_FILE = "EventsJP2025.xlsx"

def save_workbook(workbook):   
    try:
        workbook.save(EXCEL_FILE)
    except: 
        print("Close Excel you imbecile!")
        time.sleep(15)
        save_workbook(workbook)
        
def convert_to_romaji(japanese_text):
    kks = pykakasi.kakasi()
    result = kks.convert(japanese_text)
    romaji_text = ''.join([item['hepburn'] for item in result])
    return romaji_text

def doc_from_url(url):
    pagePia = requests.get(url)
    pagePia.encoding = 'utf-8'
    html_content_Pia = pagePia.text
    return BeautifulSoup(html_content_Pia, "html.parser")

def OpenSheet(sheet_name, header):
    if os.path.exists(EXCEL_FILE):
        workbook = openpyxl.load_workbook(EXCEL_FILE)
    else:
        workbook = openpyxl.Workbook()
        workbook.remove(workbook.active)
    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
    else:
        sheet = workbook.create_sheet(title=sheet_name)
        sheet.append(header) 
    sheet = workbook[sheet_name]
    return workbook, sheet
