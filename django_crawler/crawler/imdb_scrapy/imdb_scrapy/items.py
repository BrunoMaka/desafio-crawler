# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html


import scrapy
from scrapy_djangoitem import DjangoItem
from crawler.models import Movie, History

class MovieItem(DjangoItem):
    django_model = Movie

class HistoryItem(DjangoItem):
    django_model = History
    
