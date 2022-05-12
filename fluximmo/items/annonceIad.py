# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import logging
import re
import scrapy

from scrapy.loader.processors import Compose, MapCompose, TakeFirst
from fluximmo.items.annonce import Annonce

logger = logging.getLogger(__name__)

class AnnonceIad(Annonce):
    def add_prefix_to_url(url):
        return 'https://www.iadfrance.fr' + url

    def find_city_name(title):
        regex = r".*[a|à|á|à] (.*) \([0-9]*\)"
        matches = re.finditer(regex, title, re.MULTILINE | re.IGNORECASE)

        for matchNum, match in enumerate(matches, start=1):
            for groupNum in range(0, len(match.groups())):
                return match.group(groupNum + 1)

    photos = scrapy.Field(
        input_processor=Compose(MapCompose(add_prefix_to_url)),
        output_processor=Compose(Annonce.deduplicate_urls),
    )
    city = scrapy.Field(
        output_processor=Compose(TakeFirst(), find_city_name)
    )