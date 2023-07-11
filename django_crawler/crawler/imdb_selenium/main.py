
from selenium.webdriver import Chrome
from crawler.crawler import Crawler
from crawler.settings import *
from tools.webdriver_setup import Setup
import os, sys

class Application():
    def __init__(self, project_path, filename, filetype, history_id):   
        self.project_path = project_path 
        self.filename = filename   
        self.filetype = filetype
        self.history_id = history_id
        self.right_url = False
        self.run()   

    def run(self):
        while not self.right_url:
            setup = Setup(os.getcwd())    
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
        self.crawler.get_info(
            self.history_id
        )
        self.crawler.save_info(
            self.project_path, 
            self.filename, 
            self.filetype,            
            )
        self.crawler.save_in_db()
   

if __name__ == "__main__":    
    Application(
        sys.argv[1], 
        sys.argv[2], 
        sys.argv[3], 
        sys.argv[4]
        )
