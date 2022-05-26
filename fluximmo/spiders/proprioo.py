# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.proprioo import Proprioo
from scrapy import Request
from datetime import datetime
import pdb


logger = logging.getLogger(__name__)


class propriooSpider(CrawlSpiderFluximmo):
    name = "proprioo"  # nom du portail
    allowed_domains = ["www.proprioo.fr"]  # Domaine(s) du portail
    website = "www.proprioo.fr"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(propriooSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.proprioo\.fr\/nosannonces\/annonce\/([a-zA-Z-0-9._%]*)\/([0-9]*)\?([a-zA-Z-0-9._%=&]*)",
        )


    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            'https://www.proprioo.fr/nosannonces?status=PUBLISHED&page={page_index}'
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')
        i = ItemLoader(item=Proprioo(), response=response)
        ROOT_XPATH = "//*/body/"

        i.add_value("url", response.url) # Toujours garder tel quel
        i.add_value("public_url", response.url) # Toujours garder tel quel
        i.add_value("website", self.website) # Toujours garder tel quel
        i.add_value("is_available", True) # Toujours garder tel quel
        i.add_value("site_id", self.extract_site_id(response.url)) # Toujours garder tel quel
        i.add_value("origin", response.meta.get("origin")) # Toujours garder tel quel

        i.add_xpath("title", f'{ROOT_XPATH}/h1/text()') # Titre de l'annonce
        i.add_xpath(
            "description",
            f'{ROOT_XPATH}/*[contains(@data-test, "paragraph")]/text()',
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/*[contains(@data-test, 'main-price')]/text()")
        i.add_xpath("area", f'{ROOT_XPATH}/*[contains(@data-test, "squareFeetFilter")]/text()')

        i.add_xpath("land_surface", f'{ROOT_XPATH}/*[contains(text(), "Terrain")]/following-sibling::span/text()')

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[contains(@data-test, 'rooms-tag')]/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[contains(@data-test, 'bedrooms')]/text()")


        i.add_value("city", response.url.split("/")[-2].split("_")[-1])
        i.add_value("postal_code",response.url.split("/")[-2].split("_")[-2])


        i.add_value("agency", True)
        i.add_value("agency_name", "Proprioo")

        # fonctionne dans le browser mais le crawl ne trouve pas (peut etre chargement dynamique)
        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@src, 'picture')]/@src")
        others = []

        try:
            others.append(response.xpath(f"{ROOT_XPATH}/*[contains(@aria-label, 'performance énergétique')]/div/*[contains(@role, 'group')][1]/@aria-label").extract_first().replace(':', ' '))
        except:pass
        try:
            others.append(response.xpath(f"{ROOT_XPATH}/*[contains(@aria-label, 'performance énergétique')]/div/*[contains(@role, 'group')][2]/@aria-label").extract_first().replace(':', ' '))
        except:pass

        elems = response.xpath(f'{ROOT_XPATH}/*[contains(@data-test, "panel-content")]/ul/li/div')
        for elem in elems:
            value = " ".join([cell for cell in elem.xpath('.//text()').extract() if cell]).replace(':', ' ').strip()
            others.append(value)
        
        i.add_value(
                "others",
                others,
            )

        return i.load_item()

    """
        Extraction sur de l'UID d'une annonce à partir de son URL
    """
    @staticmethod
    def extract_site_id(url):
        url_cleaned = clean_url(url)
        return url_cleaned.split("/")[-1].split('?')[0]