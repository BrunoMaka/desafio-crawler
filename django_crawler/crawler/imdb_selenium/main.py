
from selenium.webdriver import Chrome
from crawler.crawler import Crawler
from crawler.settings import *
from tools.webdriver_setup import Setup
import os, time

class Application():
    def __init__(self):
        self.run()

    def run(self):
        setup = Setup(os.getcwd())       
        self.webdriver = Chrome(service=setup.s, options=setup.opt)
        self.crawler = Crawler(self.webdriver, MAIN_URL)
        self.crawler.open_url()
        time.sleep(1)

if __name__ == "__main__":
    Application()