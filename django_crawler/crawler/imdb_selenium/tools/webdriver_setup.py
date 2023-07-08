
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
        self.opt.add_argument('--kiosk-printing')