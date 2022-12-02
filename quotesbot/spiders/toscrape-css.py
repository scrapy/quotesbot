# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.crawler import CrawlerProcess
# from mdb import get_database
import datetime
# import pytz
# now = datetime.datetime.now(pytz.timezone('US/Pacific'))


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://www.domainbird.com.au/',
    ]

    rules = (
        Rule(LinkExtractor(allow_domains=['domainbird.com.au']), follow=True, callback="parse_item"),
    )

    def parse_item(self, response):
        address = response.url
        count_address = len(address)
        content_type = response.headers['Content-Type']
        status_code = response.status
        title = response.xpath("//title/text()").extract()
        count_title = len(title[0])
        description = response.xpath("//meta[@name='description']/@content").extract_first()
        if description:
            count_description = len(description)
        else:
            count_description = 0
        keywords = response.xpath("//meta[@name='keywords']/@content").extract_first()
        h1 = response.xpath('//h1//text()').extract_first()
        h2 = response.xpath('//h2//text()').extract_first()
        robot = response.xpath("//meta[@name='robots']/@content").extract_first()
        download_time = response.meta['download_latency']
        yield {
            'Address': address,
            'Address count': count_address,
            'Content Type': content_type,
            'Status code': status_code,
            'Title': title,
            'Title count': count_title,
            'Meta description': description,
            'Meta description count': count_description,
            'Meta keywords': keywords,
            'H1': h1,
            'H2': h2,
            'Robot': robot,
            'Download time': download_time
        }


# class ToScrapeCSSSpider(scrapy.Spider):
#     name = "toscrape-css"
#     start_urls = [
#         'http://quotes.toscrape.com/',
#     ]

#     def parse(self, response):
#         for quote in response.css("div.quote"):
#             yield {
#                 'text': quote.css("span.text::text").extract_first(),
#                 'author': quote.css("small.author::text").extract_first(),
#                 'tags': quote.css("div.tags > a.tag::text").extract()
#             }

#         next_page_url = response.css("li.next > a::attr(href)").extract_first()
#         if next_page_url is not None:
#             yield scrapy.Request(response.urljoin(next_page_url))

