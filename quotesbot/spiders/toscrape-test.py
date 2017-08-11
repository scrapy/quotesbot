# -*- coding: utf-8 -*-
import scrapy

class ToScrapeHTMLSpider(scrapy.Spider):
    name = "toscrape-html"
    start_urls = [
        'http://quotes.toscrape.com/'
]

    def parse(self, response):
        for quote in response.html("
