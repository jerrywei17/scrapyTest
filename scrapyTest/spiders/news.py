import scrapy
from ..items import TranewsItem
from scrapy.exceptions import CloseSpider


class NewsSpider(scrapy.Spider):
    name = "news"
    num = 1
    start_urls = [
        "http://blog.tranews.com/blog/category/%E6%97%85%E9%81%8A",
        "http://blog.tranews.com/blog/%E7%BE%8E%E9%A3%9F",
        "http://blog.tranews.com/blog/%E8%97%9D%E6%96%87",
        "http://blog.tranews.com/blog/%E4%BC%91%E9%96%92",
    ]

    def parse(self, response):
        for t in response.css("h2.entry-title"):
            link = t.css("a::attr(href)").extract_first()
            title = t.css("a::text").extract_first()
            meta = {
                "link": link,
                "title": title,
            }
            yield scrapy.Request(link, callback=self.article_parser, meta=meta)
        self.num += 1
        if self.num < 3:
            next_page = self.start_urls[0] + "/page/" + str(self.num)
        else:
            raise CloseSpider("close it")
        yield scrapy.Request(next_page, callback=self.parse)
        pass

    def article_parser(self, response):
        article = TranewsItem()
        article["title"] = response.meta["title"]
        article["link"] = response.meta["link"]

        contents = response.css(".entry-content p::text").extract()[1:]
        article["content"] = ",".join(contents)
        article["img"] = response.css("img::attr(src)").extract_first()
        article["time"] = response.css("span.entry-date::text").extract_first()
        return article
