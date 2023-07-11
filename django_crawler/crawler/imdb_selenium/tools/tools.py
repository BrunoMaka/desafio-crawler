

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import logging, os
from abc import ABC
from crawler.settings import *
from crawler.locators import * 


class Tools(ABC):   
    def __init__(self, webdriver, url):       
        self.webdriver = webdriver       
        self.webdriver.maximize_window()        
        self.url = url    
        self.setup_log()  

    def print_log(self, msg):
        '''
        escreve o log no cmd e no log
        '''
        print(msg)
        logging.info(msg)  

    def setup_log(self):     
        '''
        faz o setup do log
        '''   
        logging.basicConfig(
            filename =  os.getcwd() + f"\\crawler\\imdb_selenium\\imdb.log", 
            level = logging.INFO, 
            filemode='w', 
            encoding='utf8',
            format = "%(asctime)s :: %(message)s",
            datefmt = '%d-%m-%Y %H:%M:%S') 

    def wait_(self, t=60):
        '''
        aguarda por t segundos
        '''
        return WebDriverWait(self.webdriver, t)
        
    def wait_element(self, locator, t=60, el_type='presence'):      
        '''
        aguarda elemento por t segundos de acordo com e expect conditions definido
        '''
        if el_type == 'presence':
            return self.wait_(t).until(EC.presence_of_element_located(locator))
        elif el_type == 'clickable':
            return self.wait_(t).until(EC.element_to_be_clickable(locator))
        elif el_type == 'visibility':
            return self.wait_(t).until(EC.visibility_of_element_located(locator))
    
    def find(self, locator, t=60, el_type='presence'): 
        '''
        retorna o elemento
        '''       
        self.wait_element(locator, t, el_type)
        return self.webdriver.find_element(*locator)
    
    def finds(self, locator, t=60, el_type='presence'):  
        '''
        retorna os elementos
        '''      
        self.wait_element(locator, t, el_type)
        return self.webdriver.find_elements(*locator)    
        
    def open_url(self):        
        '''
        abre a url
        '''
        self.webdriver.get(self.url)        

    def click_in_element(self, locator, t=60, el_type='presence'):     
        '''
        clica no elemento
        '''   
        self.find(locator, t, el_type).click()    
    
    def click_in_elements(self, locator, i, t=60, el_type='presence'):    
        '''
        encontra os elementos e clica no elemento posicionado no index
        '''    
        elements = self.finds(locator, t, el_type)
        elements[i].click()

    def send_keys_to_element(self, locator, keys, t=60, el_type='presence'):    
        '''
        envia texto para o elemento
        '''    
        self.find(locator, t, el_type).send_keys(keys)

    def send_keys_to_elements(self, locator, i, keys, t=60, el_type='presence'):
        '''
        encia texto para o elemento na posição definida
        '''        
        elements = self.finds(locator, t, el_type)
        elements[i].send_keys(keys)
     
    def switch_to_frame(self, to): 
        '''
        altera para o frame
        '''       
        return self.webdriver.switch_to.frame(to)
    
    def switch_to_default_content(self):     
        '''
        altera para o conteudo default
        '''   
        return self.webdriver.switch_to.default_content()

    def switch_to_parent_frame(self):       
        '''alterna para o frame pai
        '''
        return self.webdriver.switch_to.parent_frame()
    
    def split_list(self, list, num):  
        '''
        divide uma lista de acordo com o num informado
        '''            
        splited_list = []
        a = int(len(list) / num)
        len_l = len(list)
        for i in range(a):
            start = int(i*len_l/a)
            end = int((i+1)*len_l/a)
            splited_list.append(list[start:end])
        return splited_list
    
    def create_list(self, tag):    
        '''
        clica uma lista de acordo com o tag informado
        '''    
        req = self.webdriver.page_source
        soup = BeautifulSoup(req, 'html.parser')
        tags = soup.find_all(tag)
        lista = []
        for t in tags:
            lista.append(t.text.strip())
            lista = list(filter(('').__ne__, lista))
        return lista
    
    