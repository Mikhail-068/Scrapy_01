import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['parsemachine.com']
    start_urls = ['http://parsemachine.com/']

    def parse(self, response):
        pass
