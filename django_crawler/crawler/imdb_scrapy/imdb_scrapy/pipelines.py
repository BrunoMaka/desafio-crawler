# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector, re, os, logging


class MySQLPipeline(object):
    '''
    Pipeline para manipular tabelas MySQL
    '''
    def __init__(self, db_host, db_user, db_passwd, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_name = db_name

    @classmethod
    def from_crawler(cls, crawler):
        db_settings = crawler.settings.getdict("DB_SETTINGS")
        return cls(
            db_host=db_settings['MYSQL_HOST'],
            db_user=db_settings['MYSQL_USER'],
            db_passwd=db_settings['MYSQL_PASSWORD'],
            db_name=db_settings['MYSQL_DATABASE'])
    
    def open_spider(self, spider):
        '''
        Ao iniciar o spider, é criada o banco de dados caso não exista
        '''
        self.db = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            passwd=self.db_passwd
        )
        self.cursor = self.db.cursor()

        create_database_query = f"CREATE DATABASE IF NOT EXISTS {self.db_name}"
        self.cursor.execute(create_database_query)
        self.db.commit()

        self.db = mysql.connector.connect(
            host=self.db_host,
            user=self.db_user,
            passwd=self.db_passwd,
            database=self.db_name
        )
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
        
