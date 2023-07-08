#pip install sqlalchemy
#pip install pymysql
#import sqlalchemy, os

'''ENGINE = sqlalchemy.create_engine(
    f'mysql+pymysql://{os.environ["DATABASE_USERNAME"]}:{os.environ["DATABASE_PASSWORD"]}@{os.environ["DATABASE_HOST"]}/{os.environ["DATABASE_SGBD"]}')'''

MAIN_URL = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'

CRAWLER_NAME = 'crawler_imdb_selenium'