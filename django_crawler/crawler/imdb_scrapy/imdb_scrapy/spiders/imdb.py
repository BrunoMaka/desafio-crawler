import scrapy
from scrapy.settings import Settings


class ImdbSpider(scrapy.Spider):        
    name = "imdb"   
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'pt-BR'
    }
   
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        for movie in response.css('.ipc-metadata-list-summary-item.sc-bca49391-0.eypSaE.cli-parent'):
            yield {
                'posicao': movie.css('h3.ipc-title__text::text').get().split('.')[0],
                'filme': movie.css('h3.ipc-title__text::text').get().split('.')[1],
                'ano': movie.css('span.sc-14dd939d-6.kHVqMR.cli-title-metadata-item::text').getall()[0],
                'duracao': movie.css('span.sc-14dd939d-6.kHVqMR.cli-title-metadata-item::text').getall()[1],
                'classificacao_idade': movie.css('span.sc-14dd939d-6.kHVqMR.cli-title-metadata-item::text').getall()[2],
                'nota': movie.css('div[data-testid="ratingGroup--container"] span::text').get()
            }

