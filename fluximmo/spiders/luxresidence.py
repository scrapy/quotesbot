# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.annonce import Annonce
from scrapy import Request
from datetime import datetime
import pdb


logger = logging.getLogger(__name__)


class luxResidenceSpider(CrawlSpiderFluximmo):
    name = "luxresidence"  # nom du portail
    allowed_domains = ["www.lux-residence.com"]  # Domaine(s) du portail
    website = "www.lux-residence.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(luxResidenceSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.lux-residence\.com\/fr\/vente\/([a-zA-Z-0-9.]*)\/france\/.*",
        )


    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            # fonctionnait au début de mes test mais ne semble plus fonctionner (site dynamique ?)
            'https://www.lux-residence.com/fr/search?idtt=2&idpays=250&tri=DatePublicationAntechronologique&idtb=2,1,13,14,9,4&idstb=1,27,52,10,2&p={page_index}'
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')
        i = ItemLoader(item=Annonce(), response=response)
        ROOT_XPATH = "//*/body/"

        i.add_value("url", response.url) # Toujours garder tel quel
        i.add_value("public_url", response.url) # Toujours garder tel quel
        i.add_value("website", self.website) # Toujours garder tel quel
        i.add_value("is_available", True) # Toujours garder tel quel
        i.add_value("site_id", self.extract_site_id(response.url)) # Toujours garder tel quel
        i.add_value("origin", response.meta.get("origin")) # Toujours garder tel quel

        i.add_xpath("title", f'{ROOT_XPATH}/*[contains(@class, "city")]/text()') # Titre de l'annonce
        i.add_xpath(
            "description",
            f'{ROOT_XPATH}/*[contains(@id, "descriptionSection")]/span/text()',
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/*[contains(@class, 'informationSale')]//text()")
        i.add_xpath("area", f'{ROOT_XPATH}/*[contains(@class, " area")]//text()')

        i.add_value("land_surface", "")

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[contains(@class, ' nbrRoom')]//text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[contains(@class, ' nbrBedroom')]//text()")

        i.add_value("postal_code", "")
        i.add_xpath("city", f"{ROOT_XPATH}/*[contains(@class, 'city')]/text()")


        i.add_value("agency", True)
        i.add_value("agency_name", "Lux-residence")

        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@class, 'slider animated')]/li//@src")

        i.add_xpath(
            "others",
            f"{ROOT_XPATH}/*[contains(@class, 'listBlock')]/li//text()",
        )

        others = []
        try:
            others.append("DPE " + response.xpath(f"{ROOT_XPATH}/*[contains(@data-testid, 'dpeClasseActive')]/text()").extract_first())
        except:pass
        try:
            others.append("GES " + response.xpath(f"{ROOT_XPATH}/*[contains(@data-testid, 'gesClasseActive')]/text()").extract_first())
        except:pass

        i.add_value("others", others)
        

        i.add_xpath(
            "others",
            f"{ROOT_XPATH}/*[contains(@class, 'listBlock')]/li//text()",
        )

        return i.load_item()

    """
        Extraction sur de l'UID d'une annonce à partir de son URL
    """
    @staticmethod
    def extract_site_id(url):
        url_cleaned = clean_url(url)
        return url_cleaned.split("/")[-2]