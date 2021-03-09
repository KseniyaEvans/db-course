from scrapy.http.response import Response
import scrapy

class UkraineIsSpider(scrapy.Spider):
    name = 'ukraine-is'
    start_urls = [
        'https://www.ukraine-is.com/uk/']
    
    def parse(self, response: Response):
        image_elements = response.xpath("//img/@src[starts-with(., 'http')]")
        text_elements = response.xpath(
            "//*[not(self::script)][not(self::style)][string-length(normalize-space(text())) > 30]/text()")
        yield {
            'url': response.url,
            'payload': 
            [
                {
                    'type': 'text',
                    'data': text.get().strip()
                } for text in text_elements
            ] +
            [
                {
                    'type': 'image',
                    'data': image.get()
                } for image in image_elements
            ]
        }
        if response.url == self.start_urls[0]:
            link_elems = response.xpath("//a/@href[starts-with(., 'https://www.ukraine-is.com/uk/') or starts-with(., '/')]")
            links = [link.get() for link in link_elems if link.get() != "https://www.ukraine-is.com/uk/"][:19]            
            for link in links:
                yield scrapy.Request(link, self.parse)

