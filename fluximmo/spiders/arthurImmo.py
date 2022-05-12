# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.annonce import Annonce

logger = logging.getLogger(__name__)


class ArthurImmoSpider(CrawlSpiderFluximmo):
    name = "arthurimmo"  # nom du portail
    allowed_domains = ["www.arthurimmo.com"]  # Domaine(s) du portail
    website = "www.arthurimmo.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(ArthurImmoSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.arthurimmo\.com\/annonce\/(location|achat|vente)\/([a-zA-Z-0-9]*)\/([a-zA-Z-0-9]*)-([a-zA-Z-0-9]*)\/r([0-9]*)",
        )

    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            'https://www.arthurimmo.com/recherche,basic.htm?transactions=acheter&types%5B0%5D=maison&types%5B1%5D=appartement&types%5B2%5D=terrain&types%5B3%5D=immeuble&types%5B4%5D=local-commercial&types%5B5%5D=boutique&types%5B6%5D=parking&types%5B7%5D=bureau&page={page_index}',
            'https://www.arthurimmo.com/recherche,basic.htm?transactions=louer&types%5B0%5D=maison&types%5B1%5D=appartement&types%5B2%5D=terrain&types%5B3%5D=immeuble&types%5B4%5D=local-commercial&types%5B5%5D=boutique&types%5B6%5D=fonds-de-commerce&types%5B7%5D=parking&types%5B8%5D=bureau&sort=-updated_at&page={page_index}'
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

        i.add_xpath("title", f'{ROOT_XPATH}/h1/text()') # Titre de l'annonce
        i.add_xpath(
            "description",
            f'{ROOT_XPATH}/div[1]/div[2]/div[2]/div[4]/div[1]/div[1]/div[2]/div/p//text()',
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/div[1]/div[2]/div[2]/div[2]/div/div[1]//text()")
        i.add_xpath("area", f'{ROOT_XPATH}/ul/li/*[contains(text(), "Surface habitable")]/../*[contains(text(), "m²")]/text()')

        i.add_xpath("land_surface", f'{ROOT_XPATH}/ul/li/*[contains(text(), "Surface terrain")]/../*[contains(text(), "m²")]/text()')

        i.add_xpath("rooms", f"{ROOT_XPATH}/ul/li/*[contains(text(), 'pièces')]/../div[2]/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/ul/li/*[contains(text(), 'chambres')]/../div[2]/text()")

        i.add_value("postal_code", response.url.split('/')[-2].split('-')[1])
        i.add_value("city", response.url.split('/')[-2].split('-')[0])

        i.add_value("agency", True)
        i.add_value("agency_name", "Arthurimmo")

        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@href, 'photos.')]/@src")
        return i.load_item()

    """
        Extraction sur de l'UID d'une annonce à partir de son URL
    """
    @staticmethod
    def extract_site_id(url):
        url_cleaned = clean_url(url)
        return url_cleaned.split("/")[-1].split(".")[0]