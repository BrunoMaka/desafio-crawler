
from selenium.webdriver import Chrome
from crawler.crawler import Crawler
from crawler.settings import *
from tools.webdriver_setup import Setup
import os, sys, time

class Application():
    def __init__(self, project_path, filename, filetype):   
        self.project_path = project_path 
        self.filename = filename   
        self.filetype = filetype
        #self.history_id = history_id
        self.right_url = False
        self.run()   

    def run(self):
        '''
        enquanto não encontra a url no layout correto, fecha o webdriver e cria outro
        após encontrar, faz a coleta, salva o arquivo no formato indicado e salva as 
        informações no banco de dados
        '''
        inicio = time.time()    
        while not self.right_url:
            setup = Setup(self.project_path)    
            self.webdriver = Chrome(
                service=setup.s, 
                options=setup.opt)     
            self.crawler = Crawler(
                self.webdriver, 
                MAIN_URL)
            self.crawler.print_log(f'Abrindo URL') 
            self.crawler.open_url()
            if not self.crawler.is_right_url():    
                self.crawler.print_log(f'URL está com layout errado. Recarregando url')           
                self.webdriver.quit()
            else:
                self.right_url = True
        self.crawler.print_log(f'Iniciando a coleta') 
        self.webdriver.save_screenshot('screenshot.png')  
        history_id = self.crawler.create_history(self.filetype)   
        self.crawler.get_info(
            #self.history_id
            history_id
        )
        self.crawler.save_info(
            self.project_path, 
            self.filename, 
            self.filetype,            
            )
        time.sleep(1)
        fim = time.time()  
        tempo_total = fim - inicio 
        self.crawler.save_in_db(history_id, tempo_total, self.project_path)
   

if __name__ == "__main__":        
    Application(
        os.getcwd(),#sys.argv[1], #path do projeto - os.getcwd()
        'imdb',#sys.argv[2], #nome - imdb
        sys.argv[1], #tipo de arquivo - csv
        #sys.argv[4]  #historico
        )
