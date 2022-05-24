# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.efficity import Efficity
import pdb

logger = logging.getLogger(__name__)


class EffiCitySpider(CrawlSpiderFluximmo):
    name = "efficity"  # nom du portail
    allowed_domains = ["www.efficity.com"]  # Domaine(s) du portail
    website = "www.efficity.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(EffiCitySpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.efficity\.com\/achat-immobilier\/(maison|appartement)([a-zA-Z-0-9-_]*)\/",
        )

    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            'https://www.efficity.com/achat-immobilier/results/?inputed_location=4084%2C4027%2C4053%2C4024&typeahed_inputed_location=&property_type=1&property_type=2&property_type=4&property_type=5&property_type=7&min_price=&max_price=&min_living_area=&max_living_area=&min_nb_of_rooms=0&order_by=0&page={page_index}'

            'https://www.efficity.com/achat-immobilier/results/?inputed_location=4094%2C4044%2C4032%2C4011&typeahed_inputed_location=&property_type=1&property_type=2&property_type=4&property_type=5&property_type=7&min_price=&max_price=&min_living_area=&max_living_area=&min_nb_of_rooms=0&order_by=0&page={page_index}'

            'https://www.efficity.com/achat-immobilier/results/?inputed_location=4028%2C4075%2C4076%2C4052&typeahed_inputed_location=&property_type=1&property_type=2&property_type=4&property_type=5&property_type=7&min_price=&max_price=&min_living_area=&max_living_area=&min_nb_of_rooms=0&order_by=0&page={page_index}'

            'https://www.efficity.com/achat-immobilier/results/?inputed_location=4093&typeahed_inputed_location=&property_type=1&property_type=2&property_type=4&property_type=5&property_type=7&min_price=&max_price=&min_living_area=&max_living_area=&min_nb_of_rooms=0&order_by=0&page={page_index}'
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')
        i = ItemLoader(item=Efficity(), response=response)
        ROOT_XPATH = "//*/body/"

        i.add_value("url", response.url) # Toujours garder tel quel
        i.add_value("public_url", response.url) # Toujours garder tel quel
        i.add_value("website", self.website) # Toujours garder tel quel
        i.add_value("is_available", True) # Toujours garder tel quel
        i.add_value("site_id", self.extract_site_id(response.url)) # Toujours garder tel quel
        i.add_value("origin", response.meta.get("origin")) # Toujours garder tel quel

        i.add_xpath("title", f'//h1/text()') # Titre de l'annonce
        i.add_xpath(
            "description",
            f'{ROOT_XPATH}/*[contains(@class, "moar-content")]/p/text()',
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/p[contains(@class, 'details-price')]/text()")
        i.add_value("area", response.url.split('/')[-2].split('-')[0].split('_')[1])

        i.add_value("land_surface", '')

        i.add_xpath("rooms", f'//h1/text()') # Titre de l'annonce
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/ul[contains(@class, 'details')]/li//*[contains(@alt, 'chambres')]/@alt")


        loc = response.xpath('//*[contains(@class, "details-location")]/text()').extract_first().split('(')
        i.add_value("postal_code", loc[1].replace(')', '').strip())
        i.add_value("city", loc[0].strip())

        i.add_value("agency", True)
        i.add_value("agency_name", "Efficity")

        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@class, 'slick-slide slick-cloned')]//div/img[contains(@src, 'photos/l')]/@src")

        others = []
        try:
            others.append("DPE " + response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'energy-class')]//*[contains(@class, 'active')]/following-sibling::div/span/text()").extract_first() + " kWh/m².an")
        except:pass
        try:
            others.append("GES " + response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'climate-class')]//*[contains(@class, 'active')]/following-sibling::div/span/text()").extract_first() + " kgCO2/m2.an")
        except:pass


        elems = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "program-details-sideba")]/ul/li')
        for elem in elems:
            value = " ".join([cell for cell in elem.xpath('./text()').extract() if cell]).strip().replace(':', '')
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
        return url_cleaned.split("/")[-1].split("_")[-1]