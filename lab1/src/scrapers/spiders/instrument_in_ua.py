from scrapy.http.response import Response
import scrapy


class InstrumentInUaSpider(scrapy.Spider):
    name = 'instrument_in_ua'
    start_urls = ['https://instrument.in.ua/katalog/']

    def parse(self, response: Response):
        products = response.xpath("//li[contains(@class, 'catalog-grid__item')]")[:20]
        
        for product in products:
            yield {
                'description': product.xpath(".//div[@class='catalogCard-title']/a[@title]/text()").get().strip(),
                'price': product.xpath(".//div[@class='catalogCard-price' or @class='catalogCard-price __light']/text()").get().strip(),
                'img': 'https://instrument.in.ua' + product.xpath(".//img[@class='catalogCard-img']/@src").get().strip()
            }

