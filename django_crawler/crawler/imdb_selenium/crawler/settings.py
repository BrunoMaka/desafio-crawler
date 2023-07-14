import os
from dotenv import load_dotenv
from pathlib import Path

'''dotenv_path = Path(__file__).resolve().parent.parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)'''

MAIN_URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

CRAWLER_NAME = 'crawler_imdb_selenium'

'''DB_SETTINGS = {
    'MYSQL_HOST': os.environ['DB_HOST'],
    'MYSQL_USER': os.environ['DB_USER'],
    'MYSQL_PASSWORD': os.environ['DB_PASSWORD'],
    'MYSQL_DATABASE': os.environ['DB_NAME'],
}'''