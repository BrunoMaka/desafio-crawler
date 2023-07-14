from tools.tools import Tools
import sqlite3, os
from .locators import *
import pandas as pd
from datetime import datetime
from pathlib import Path


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
        path =  os.path.join(project_path, f'{filename}.{file_type}')
        
        if file_type == 'csv':        
            df.to_csv(path, index=False)
        elif file_type == 'json':
            df.to_json(path, orient="records")

    def save_in_db(self, history_id, tempo, project_path):     
        '''
        Salva as informações na tabela do banco de dados
        '''
        self.print_log('Incluindo itens ao banco de dados')   

        # Estabelece a conexão com o banco de dados SQLite
        db_path = str(Path(__file__).resolve().parent.parent.parent.parent / 'db.sqlite3')
        conexao = sqlite3.connect(db_path)
        #conexao = sqlite3.connect(os.path.dirname(os.getcwd() + '\\db.sqlite3'))
        cursor = conexao.cursor()

        for item in self.items:
            campos = ', '.join(item.keys())
            valores = ', '.join([f"'{valor}'" for valor in item.values()])
            consulta = f"INSERT INTO crawler_movie ({campos}) VALUES ({valores})"        
            cursor.execute(consulta)
        conexao.commit()

        query_tempo = f'UPDATE crawler_history SET tempo_de_coleta = {tempo} WHERE id = {history_id}'
        cursor.execute(query_tempo)
        conexao.commit()
        
        with open(os.path.join(project_path, 'imdb.log'), "r", encoding='utf-8') as file:
            log_content = file.read()
        query_log = f'UPDATE crawler_history SET log = "{log_content}" WHERE id = {history_id}'
        cursor.execute(query_log)
        conexao.commit()

        conexao.close()

    def create_history(self, tipo_saida):        
        db_path = str(Path(__file__).resolve().parent.parent.parent.parent / 'db.sqlite3')
        
        conexao = sqlite3.connect(db_path)
        #conexao = sqlite3.connect(os.path.dirname(os.getcwd() + '\\db.sqlite3'))
        cursor = conexao.cursor()
        query = f'''
        INSERT INTO crawler_history
        (tipo_acionamento, tipo_saida, data_acionamento, tempo_de_coleta, log)
        VALUES ('selenium', '{tipo_saida}', '{datetime.now()}', '0', '')      
        '''
        cursor.execute(query)
        conexao.commit()
        history_id = cursor.lastrowid
        conexao.close()
        return history_id
    

    def is_right_url(self):
        '''
        verifica se a url está no layout correto
        '''
        return self.find((L_HTML)).get_attribute('xmlns:og') == 'http://opengraphprotocol.org/schema/'
         

           


        