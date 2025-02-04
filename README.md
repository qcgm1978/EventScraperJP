# EventScraperJP
WebScraper for https://t.pia.jp/ and https://l-tike.com/ and https://eplus.jp/


Python + Flask + JS with Electron + HTML + CSS

Project made with love for a Uni course by Mast.
Thank you Lange and others for all the help.


To build the app (both the Python .exe and whole Electron environment) if need be for any changes to the code, I recommend to use these commands:

pyinstaller --onefile --noconsole --hidden-import=requests --hidden-import=re --hidden-import=bs4 --hidden-import=openpyxl --hidden-import=pykakasi --hidden-import=pandas --hidden-import=time --hidden-import=os --hidden-import=concurrent.futures --hidden-import=random --hidden-import=sys --hidden-import=datetime --hidden-import=openpyxl.styles --hidden-import=openpyxl.worksheet.dimensions --hidden-import=openpyxl.utils --hidden-import=openpyxl.utils.dataframe --hidden-import=flask --hidden-import=flask.json --add-data="site;site" --add-data="C:\Users\YOURUSERNAME\AppData\Local\Programs\Python\Python313\Lib\site-packages\pykakasi\data;pykakasi\data" EventScraperJP.py

//Replace YOURUSERNAME (and check the python location and pykakasi's data)//

npm run build