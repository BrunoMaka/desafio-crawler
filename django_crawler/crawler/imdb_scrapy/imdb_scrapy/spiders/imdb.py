import scrapy

class ImdbSpider(scrapy.Spider):        
    name = "imdb"   
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'pt-BR'
    }

    def __init__(self, history_id=None, *args, **kwargs):
        super(ImdbSpider, self).__init__(*args, **kwargs)
        self.history_id = history_id
   
    def start_requests(self):     
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta={'history_id': self.history_id})

    def parse(self, response):
        history_id = response.meta.get('history_id')
        for movie in response.css('.ipc-metadata-list-summary-item__tc'):
            yield {
                'position': int(movie.css('.ipc-title__text::text').get().split('.')[0]),
                'movie': movie.css('.ipc-title__text::text').get().split('.')[-1],                
                'year': movie.css('span.sc-14dd939d-6.kHVqMR.cli-title-metadata-item::text').getall()[0],
                'duration': movie.css('span.sc-14dd939d-6.kHVqMR.cli-title-metadata-item::text').getall()[1],
                'rating': movie.css('span.sc-14dd939d-6.kHVqMR.cli-title-metadata-item::text').getall()[2],
                'rate': float(movie.css('div[data-testid="ratingGroup--container"] span::text').get().replace(',', '.')),
                'history_id': history_id
            }

