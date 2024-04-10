import requests
from datetime import date
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import sqlite3


class ETL:

    def __init__(self, plaza_id, sql_file_path, sql_table_name):
        self.plaza_id = plaza_id
        self.sql_file_path = sql_file_path
        self.sql_table_name = sql_table_name
        self.url = f'https://tis.nhai.gov.in/TollInformation.aspx?TollPlazaID={plaza_id}'
        self.soup = ''
        self.df_info = pd.DataFrame()

    def extract(self):
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.text, 'html.parser')
        if self.soup.find(class_='PA15'):
            return True
        return False
    
    def transform(self):
        plaza_name = self.soup.find(class_='PA15').find_all('p')[0].find('lable')
        table_html = str(self.soup.find_all('table', class_='tollinfotbl')[0])
        df_info = pd.read_html(table_html)[0].dropna(axis=0, how='all')
        cols = df_info.columns.to_list()
        cols.insert(0, 'Date Scrapped')
        cols.insert(1, 'Plaza Name')
        cols.insert(2, 'TollPlazaID')
        df_info['Plaza Name'] = plaza_name.text
        df_info['Date Scrapped'] = date.today()
        df_info['TollPlazaID'] = self.plaza_id
        self.df_info = df_info[cols]

    def load(self):
        with sqlite3.connect(self.sql_file_path) as conn:
            self.df_info.to_sql(self.sql_table_name, conn, if_exists='append', index=False)

            # Load in CSV Format
            self.df_info.to_csv('nhai_info.csv', mode='a', index=False, header=False)

    def run_etl(self):
        if self.extract():
            self.transform()
            self.load()
            print(f"Done with ETL of plaza_id {self.plaza_id}")
        else:
            print(f"Skipped plaza_id {self.plaza_id}")