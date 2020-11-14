import scrapy
from scrapy_splash import SplashRequest


class DynamicSpider(scrapy.Spider):
    name = 'dynamic'
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        # for url in self.start_urls:
        #     yield SplashRequest(url, self.parse, args={'wait': 1})
        yield SplashRequest('http://quotes.toscrape.com/js/', self.parse, args={'wait': 0.5, 'http_method': 'GET'})

    def parse(self, response):
        quotes = response.css('div.quote span.text::text').extract_first()
        # for q in quotes:
        print(quotes)

        print('-------------------------------')
        next_page_href = response.css('li.next a::attr(href)').extract_first()
        if next_page_href:
            next_url = 'http://quotes.toscrape.com'+next_page_href
            yield SplashRequest(next_url, self.parse, args={'wait': 0.5})
