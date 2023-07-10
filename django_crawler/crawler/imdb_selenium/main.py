
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
        self.run()   

    def run(self):
        setup = Setup(os.getcwd())       
        self.webdriver = Chrome(
            service=setup.s, 
            options=setup.opt)
        self.crawler = Crawler(
            self.webdriver, 
            MAIN_URL)
        self.crawler.open_url()
        if not self.crawler.is_right_url():            
            self.webdriver.quit()
            self.run()        
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
