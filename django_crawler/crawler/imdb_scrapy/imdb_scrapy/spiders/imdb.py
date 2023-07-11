import scrapy, logging

class ImdbSpider(scrapy.Spider):           
    name = "imdb"   
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'pt-BR'
    }

    def __init__(self, history_id=None, *args, **kwargs):
        '''
        o id do histórico é passado como argumento para vincular a coleta à este histórico
        '''
        super(ImdbSpider, self).__init__(*args, **kwargs)
        self.history_id = history_id
  
    def start_requests(self):   
        '''
        Inicia o log e o spider, conforme url definida, passando o id para o request
        '''
        logger = logging.getLogger()
        logger.info("Iniciando o spider...")  
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse, meta={'history_id': self.history_id})
   
    def parse(self, response):
        '''
        coleta as informações em um item
        '''
        history_id = response.meta.get('history_id')
        for movie in response.css('.ipc-metadata-list-summary-item__tc'):
            pos_mov = movie.css('.ipc-title__text::text').get()
            others = movie.css('span.sc-14dd939d-6.kHVqMR.cli-title-metadata-item::text').getall()   
            rate = movie.css('div[data-testid="ratingGroup--container"] span::text').get().replace(',', '.')        
            yield {
                'position': int(pos_mov.split('.')[0]),
                'movie': self.handdle_movie(pos_mov),                
                'year': others[0],
                'duration': others[1],
                'rating': others[2],
                'rate': float(rate),
                'history_id': history_id
            }

    def handdle_movie(self, text):
        '''
        trata o nome do filme, juntando todas as informações que estão após o '.'
        foi necessário fazer um replace de "'", pois há um filme que não é aceito com este caracter
        '''
        return ''.join(text.split('.')[1:]).strip().replace("'", "")


