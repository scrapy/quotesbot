# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import logging

import scrapy
from scrapy.loader.processors import TakeFirst

logger = logging.getLogger(__name__)


class UrlFoundItem(scrapy.Item):
    url = scrapy.Field(output_processor=TakeFirst())
    page_ind = scrapy.Field(output_processor=TakeFirst())
    tag = scrapy.Field(output_processor=TakeFirst())
    branch = scrapy.Field(output_processor=TakeFirst())
    is_new = scrapy.Field(output_processor=TakeFirst())
    metadata = scrapy.Field(output_processor=TakeFirst())
