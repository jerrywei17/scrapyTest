import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/login"]

    def parse(self, response):
        token = response.css("input[name='csrf_token']::attr('value')").extract_first()
        data = {"csrf_token": token, "username": "user", "password": "123"}
        yield scrapy.FormRequest(url=self.start_urls[0], formdata=data, callback=self.parse_quotes)
        pass

    def parse_quotes(self, response):
        item = {}
        for q in response.css("div.quote"):
            item["author"] = q.css("small.author::text").extract_first()
            item["content"] = q.css("span.text::text").extract_first()
        return item
