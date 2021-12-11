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
            url = response.urljoin(href)  # Формируем url адреса на товары
            yield scrapy.Request(url, callback=self.parse)  # Отправляем url адрес в обработку


    def parse(self, response, **kwargs):
        techs = {} # Пройдемся по таблице
        for row in response.css('#characteristics tbody tr'): # characteristics > tbody       #characteristics > tbody > tr:nth-child(1)
            # Соберем текстовые значения ячеек
            cols = row.css('td::text').extract()
            techs[cols[0]] = cols[1]
        # В этой функции мы будем обрабатывать каждый товар
        item = {  # здесь мы будем сохр данные по каждому товару #product_amount
            'url': response.request.url,
            'title': response.css('#product_name::text').extract_first('').strip(), # передаем css селектор. Нас интересует видимый текст(::text). Извлекаем первое значение
            'price': response.css('#product_amount::text').extract_first('').strip()
            'techs': techs,
        }
        yield item
