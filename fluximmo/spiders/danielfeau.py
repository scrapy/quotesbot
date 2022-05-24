# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.annonce import Annonce
import pdb

logger = logging.getLogger(__name__)


class DanielFeauSpider(CrawlSpiderFluximmo):
    name = "danielfeau"  # nom du portail
    allowed_domains = ["www.danielfeau.com"]  # Domaine(s) du portail
    website = "www.danielfeau.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(DanielFeauSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/danielfeau\.com\/fr\/annonce-immobiliere\/([0-9]*)",
        )

    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            # ne fonctionne pas, site dynamique pour le next page
            'https://danielfeau.com/fr/recherche',
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

        i.add_xpath("title", f'//title/text()') # Titre de l'annonce
        i.add_xpath(
            "description",
            f'{ROOT_XPATH}/p[contains(@class, "comment")]/text()',
        ) # Description de l'annonce
        
        
        i.add_xpath("price", f"{ROOT_XPATH}/*[contains(@class, 'price')]/text()")
        i.add_value("area", response.xpath('//*[contains(@class, "area")]/text()').extract()[0])

        i.add_xpath("land_surface", f'{ROOT_XPATH}/em[contains(text(), "total")]/text()')

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[contains(@class, 'rooms')]/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[contains(@class, 'bedrooms')]/text()")

        # INCOMPLET , STOP ici car list des résultats dynamique, https://danielfeau.com/fr_FR/module/36/remote/getPropertyHtmlRemote?params%5Bculture%5D=fr_FR&params%5Bcurrency%5D=EUR&params%5Bproperty_id%5D=7053842
        i.add_value("postal_code", response.url.split('/')[-2].split('-')[1])
        i.add_value("city", response.url.split('/')[-2].split('-')[0])

        i.add_value("agency", True)
        i.add_value("agency_name", "Arthurimmo")

        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@href, 'photos.')]/..//@src")

        others = []
        dpeges = response.xpath(f"{ROOT_XPATH}/*[contains(@src, 'dpe.')]/@src").extract()
        if dpeges:
            others += dpeges

        elems = response.xpath(f'{ROOT_XPATH}/ul[contains(@class, "grid")]//li')
        for elem in elems:
            value = "".join([cell for cell in elem.xpath('.//text()').extract() if cell]).strip()
            print("value", value)
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
        return url_cleaned.split("/")[-1]