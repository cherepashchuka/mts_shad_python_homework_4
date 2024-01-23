import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

#https://en.wikipedia.org/wiki/List_of_films:_A

#https://en.wikipedia.org/wiki/Aaaaaaaah!


class FilmsSpider(scrapy.Spider):
    name = "films"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/Lists_of_films"]

    def parse(self, response):
        pass
