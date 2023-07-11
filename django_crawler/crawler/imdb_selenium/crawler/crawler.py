from tools.tools import Tools
import mysql.connector
from .locators import *
from .settings import DB_SETTINGS
import pandas as pd


class Crawler(Tools):
    '''
    classe principal do crawler que herda alguns métodos de Tools, para facilitar
    '''
    def get_info(self, history_id):
        '''
        coleta todas as informações em um self.items
        '''
        self.items = []
        for i, card in enumerate(self.finds(L_CARD)):
            item = {
                'position': card.find_element(By.CLASS_NAME, 'ipc-title__text').text.split('.')[0],
                'movie': self.handdle_movie(card.find_element(By.CLASS_NAME, 'ipc-title__text').text),
                'year': card.find_elements(By.CSS_SELECTOR, '.sc-14dd939d-6.kHVqMR.cli-title-metadata-item')[0].text,
                'duration': card.find_elements(By.CSS_SELECTOR, '.sc-14dd939d-6.kHVqMR.cli-title-metadata-item')[1].text,
                'rating': card.find_elements(By.CSS_SELECTOR, '.sc-14dd939d-6.kHVqMR.cli-title-metadata-item')[2].text,
                'rate': card.find_element(By.CSS_SELECTOR, 'div[data-testid="ratingGroup--container"] span').text,
                'history_id': history_id
            }            
            self.print_log(f'ADD - {item}')
            self.items.append(item)    

    def handdle_movie(self, text):
        '''
        trata o nome do filme, juntando todas as informações que estão após o '.'
        foi necessário fazer um replace de "'", pois há um filme que não é aceito com este caracter
        '''
        return ''.join(text.split('.')[1:]).strip().replace("'", "")
                 

    def save_info(self, project_path, filename, file_type):
        '''
        salva as informações em um arquivo, conforme tipo definido
        '''
        self.print_log(f'Salvando arquivos')
        df = pd.DataFrame(data=self.items)    
        if file_type == 'csv':        
            df.to_csv(f'{project_path}\\{filename}.{file_type}', index=False)
        elif file_type == 'json':
            df.to_json(f'{project_path}\\{filename}.{file_type}', orient="records")

    def save_in_db(self):     
        '''
        salva as informações na tabela do banco de dados
        '''
        self.print_log(f'Incluindo itens ao banco de dados')   
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
        '''
        verifica se a url está no layout correto
        '''
        return self.find((L_HTML)).get_attribute('xmlns:og') == 'http://opengraphprotocol.org/schema/'
         

           


        