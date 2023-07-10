from tools.tools import Tools
import mysql.connector
from .locators import *
from .settings import DB_SETTINGS
import pandas as pd


class Crawler(Tools):
    def get_info(self, history_id):
        self.items = []
        for i, card in enumerate(self.finds(L_CARD)):
            item = {
                'position': card.find_element(By.CLASS_NAME, 'ipc-title__text').text.split('.')[0],
                'movie': card.find_element(By.CLASS_NAME, 'ipc-title__text').text.split('.')[1],
                'year': card.find_elements(By.CSS_SELECTOR, '.sc-14dd939d-6.kHVqMR.cli-title-metadata-item')[0].text,
                'duration': card.find_elements(By.CSS_SELECTOR, '.sc-14dd939d-6.kHVqMR.cli-title-metadata-item')[1].text,
                'rating': card.find_elements(By.CSS_SELECTOR, '.sc-14dd939d-6.kHVqMR.cli-title-metadata-item')[2].text,
                'rate': card.find_element(By.CSS_SELECTOR, 'div[data-testid="ratingGroup--container"] span').text,
                'history_id': history_id
            }            
            print(f'ADD - {item}')
            self.items.append(item)    
                 

    def save_info(self, project_path, filename, file_type):
        df = pd.DataFrame(data=self.items)    
        if file_type == 'csv':        
            df.to_csv(f'{project_path}\\{filename}.{file_type}', index=False)
        elif file_type == 'json':
            df.to_json(f'{project_path}\\{filename}.{file_type}', orient="records")

    def save_in_db(self):        
        conexao = mysql.connector.connect(
            host=DB_SETTINGS['MYSQL_HOST'],
            database=DB_SETTINGS['MYSQL_DATABASE'],
            user=DB_SETTINGS['MYSQL_USER'],
            password=DB_SETTINGS['MYSQL_PASSWORD']
        )
        cursor = conexao.cursor()
        for item in self.items:
            campos = ', '.join(item.keys())
            valores = ', '.join([f"'{valor}'" for valor in item.values()])
            consulta = f"INSERT INTO crawler_movie ({campos}) VALUES ({valores})"        
            cursor.execute(consulta)
        conexao.commit()
        conexao.close()


    def is_right_url(self):
        return self.find((L_HTML)).get_attribute('xmlns:og') == 'http://opengraphprotocol.org/schema/'
         

           


        