# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.sothebysrealty import Sothebysrealty
import pdb

logger = logging.getLogger(__name__)


class BarnesInternationalSpider(CrawlSpiderFluximmo):
    name = "sothebysrealty"  # nom du portail
    allowed_domains = ["www.sothebysrealty-france.com"]  # Domaine(s) du portail
    website = "www.sothebysrealty-france.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(BarnesInternationalSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.sothebysrealty-france\.com\/fr\/([a-zA-Z-]*)\/([a-zA-Z-0-9]*)\/([a-zA-Z-0-9._%]*)\/",
        )


    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            'https://www.sothebysrealty-france.com/fr/vente-proprietes-de-luxe/p={page_index}?ajax=true&tri=id:DESC',
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')
        i = ItemLoader(item=Sothebysrealty(), response=response)
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
            f'{ROOT_XPATH}/*[contains(@class, "description read")]/text()',
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/*[contains(text(), 'Prix')]/following-sibling::span/text()")
        i.add_xpath("area", f'{ROOT_XPATH}/*[contains(text(), "Surface")]/following-sibling::span/text()')

        i.add_xpath("land_surface", f'{ROOT_XPATH}/*[contains(text(), "Terrain")]/following-sibling::span/text()')

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[contains(text(), 'Pièces')]/following-sibling::span/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[contains(text(), 'Chambres')]/following-sibling::span/text()")


        location = response.xpath(f"{ROOT_XPATH}/*[contains(text(), 'Ville')]/following-sibling::span/text()").extract()
        i.add_value("postal_code", location[0])
        i.add_value("city", location[0].split('(')[0].strip())

        i.add_value("agency", True)
        i.add_value("agency_name", "SothebysRealty")


        photos = response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'galleryImg')]/@src").extract()
        photo_clean = []
        for photo in photos:
            if "sothebysrealty-france.com" not in photo:
                photo_clean.append("https://www.sothebysrealty-france.com" + photo)
            else:
                photo_clean.append(photo)
        i.add_value("photos", photo_clean)

        others = []

        elems = response.xpath(f'{ROOT_XPATH}/ul[contains(@class, "colonne_blue")]//li')
        for elem in elems:
            value = " ".join([cell for cell in elem.xpath('.//text()').extract() if cell]).strip().replace(':', '')
            others.append(value)
        

        diags = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "diagPreview__value")]/text()').extract()
        for diag in diags:
            if "kWhEP" in diag:
                diagname = "DPE"
            else:
                diagname = "GES"
            others.append(diagname + " " + diag)

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
        return url_cleaned.split("/")[5]