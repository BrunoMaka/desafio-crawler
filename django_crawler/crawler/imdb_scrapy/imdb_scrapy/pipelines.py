# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os, sqlite3



class MySQLPipeline(object):
    '''
    Pipeline para manipular tabelas MySQL
    '''
        
    def open_spider(self, spider):
        '''
        Criar conexão com banco de dados
        '''
        path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'db.sqlite3')           
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()      
        
    def process_item(self, item, spider):
        '''
        Durante a extração de dados, o item é inserido dentro da tabela
        '''               
        self.insert_data(item)  
        return item   
        
    
    def insert_data(self, item):    
        '''
        Insere o item dentro da tabela
        '''       
        columns = ', '.join(item.keys())
        values = tuple(item.values())        
        insert_query = f"INSERT INTO crawler_movie ({columns}) VALUES {values}"  
        self.cursor.execute(insert_query)
        self.db.commit()         
        

    def close_spider(self, spider):  
        '''
        fecha o conector do banco de dados
        '''      
        self.db.close()  
        
