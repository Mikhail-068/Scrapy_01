import scrapy


class CatalogSpider(scrapy.Spider):
    name = 'catalog'
    allowed_domains = ['parsemachine.com']
    start_urls = ['http://parsemachine.com/']
    pages_count = 10

    def start_requests(self):
        for page in range(1, 1 + self.pages_count):
            url = f'https://parsemachine.com/sandbox/catalog/?page={page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        # Вызываем метод CSS передаем css_селектор. Нас интересует атрибут 'href' (extract - извлекаем)
        for href in response.css('.product-card .title::attr("href")').extract():
            url = response.urljoin(href) # Формируем url адреса на товары
            yield scrapy.Request(url, callback=self.parse) # Отправляем url адрес в обработку

    def parse(self, response, **kwargs):
        pass