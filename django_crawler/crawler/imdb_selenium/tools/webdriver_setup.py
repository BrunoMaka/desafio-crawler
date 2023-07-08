
#pip install selenium
#pip install webdriver-manager

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions

class Setup():
    def __init__(self, download_path) -> None:       
        self.s = Service(ChromeDriverManager().install())  
        self.opt = ChromeOptions()               
        prefs = {
            "download.default_directory" : download_path,         
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1, 
            "safebrowsing.disable_download_protection": True,           
            }
        self.opt.add_experimental_option("excludeSwitches", ["enable-logging"])        
        self.opt.add_experimental_option("prefs", prefs)
        self.opt.add_argument("--headless")
        self.opt.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
        self.opt.add_argument("--lang=pt-BR")
        self.opt.add_argument('--disable-gpu')
        self.opt.add_argument('--disable-extensions')
        self.opt.add_argument('--no-sandbox')
        
        