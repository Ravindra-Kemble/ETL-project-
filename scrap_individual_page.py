import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import sqlite3

conn = sqlite3.connect('nhai_info.db')
c = conn.cursor()

url = requests.get('https://tis.nhai.gov.in/TollInformation.aspx?TollPlazaID=236')
soup = BeautifulSoup(url.text, 'html.parser')
plaza_name = soup.find(class_='PA15').find_all('p')[0].find('lable')
table = soup.find_all('table', class_='tollinfotbl')[0]
x = str(table)
y = pd.read_html(x)[0].dropna(axis=0, how='all')
cols = y.columns.to_list()
cols.insert(0, 'Date Scrapped')
cols.insert(1, 'Plaza Name')
y['Plaza Name'] = plaza_name.txt
y['Date Scrapped'] = date.today()
y = y[cols]
y.to_sql('nhai_info.db', conn, if_exists='append', index=False)
print(plaza_name.text)