# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.annonceIad import AnnonceIad

logger = logging.getLogger(__name__)

class IadFranceSpider(CrawlSpiderFluximmo):
    name = "iadfrance"  # nom du portail
    allowed_domains = ["iadfrance.fr"]  # Domaine(s) du portail
    website = "iadfrance.fr"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(IadFranceSpider, self).__init__(*args, **kwargs)

        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.iadfrance\.fr\/annonce\/([a-zA-Z-0-9]*)-(location|achat|vente)-([a-zA-Z-0-9]*)\/r([0-9]*)",
        )

    def generate_all_urls(self):
        return [
            'https://www.iadfrance.fr/annonces/location?page={page_index}',
            'https://www.iadfrance.fr/annonces/vente?page={page_index}'
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')

        i = ItemLoader(item=AnnonceIad(), response=response)

        ROOT_XPATH = "//*[@id='advertisement']/"

        i.add_value("url", response.url)
        i.add_value("public_url", response.url)
        i.add_value("website", self.website)
        i.add_value("is_available", True)
        i.add_value("site_id", self.extract_site_id(response.url))
        i.add_value("origin", response.meta.get("origin"))

        i.add_xpath("title", f'{ROOT_XPATH}div[1]/div[1]/h1//text()')
        i.add_xpath(
            "description",
            f'{ROOT_XPATH}/div[@class="addescription"]//p//text()',
        )

        i.add_xpath("price", f"{ROOT_XPATH}/*[@class='items-start justify-start row']//div[@class='adPrice text-darkblue text-h3']//text()")
        i.add_xpath("area", f"{ROOT_XPATH}/*[@class='items-start justify-start row']//div[@class='i-badge i-badge--square']//div[contains(text(),'m²')]/text()")
        i.add_xpath("land_surface", f"{ROOT_XPATH}/*[@class='items-start justify-start row']//div[contains(@class, 'adfeature')]//*[contains(text(), 'terrain')]/text()")

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[@class='items-start justify-start row']//div[contains(@class, 'i-badge i-badge--square')]//*[contains(text(), 'pièces')]/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[@class='items-start justify-start row']//div[contains(@class, 'i-badge i-badge--square')]//*[contains(text(), 'chambre')]/text()")

        i.add_xpath("postal_code", f'{ROOT_XPATH}div[1]/div[1]/h1//text()')
        i.add_xpath("city", f'{ROOT_XPATH}div[1]/div[1]/h1//text()')

        i.add_value("agency", True)
        i.add_value("agency_name", "IADFrance")

        i.add_xpath(
            "others",
            f"{ROOT_XPATH}/*[@class='items-start justify-start row']//div[contains(@class, 'i-badge--label-right')]//text()",
        )
        i.add_xpath(
            "others",
            f"{ROOT_XPATH}/*[@class='items-start justify-start row']//div[contains(@class, 'adfeature')]//text()",
        )
        i.add_xpath(
            "photos",
            f"{ROOT_XPATH}/*[@class='items-start justify-start row']//a[contains(@class, 'picturelink')]/@href",
        )
        return i.load_item()

    """
     Extraction sur de l'UID d'une annonce à partir de son URL
    """
    @staticmethod
    def extract_site_id(url):
        url_cleaned = clean_url(url)
        return url_cleaned.split("/")[-1].split(".")[0]