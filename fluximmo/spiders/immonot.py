# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.immonot import Immonot
from scrapy import Request
from datetime import datetime
import pdb


logger = logging.getLogger(__name__)


class immonotSpider(CrawlSpiderFluximmo):
    name = "immonot"  # nom du portail
    allowed_domains = ["www.immonot.com"]  # Domaine(s) du portail
    website = "www.immonot.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(immonotSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.immonot\.com\/annonce-immobiliere\/([a-zA-Z-0-9._%]*)\/([a-zA-Z-0-9._%]*).html",
        )


    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            'https://www.immonot.com/immobilier/tout/immobilier-notaire-p-{page_index}.html'
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')
        i = ItemLoader(item=Immonot(), response=response)
        ROOT_XPATH = "//*/body/"

        i.add_value("url", response.url) # Toujours garder tel quel
        i.add_value("public_url", response.url) # Toujours garder tel quel
        i.add_value("website", self.website) # Toujours garder tel quel
        i.add_value("is_available", True) # Toujours garder tel quel
        i.add_value("site_id", self.extract_site_id(response.url)) # Toujours garder tel quel
        i.add_value("origin", response.meta.get("origin")) # Toujours garder tel quel

        title = response.xpath('//h2/text()').extract()
        i.add_value("title", title[0].strip().replace('\xa0', '')) # Titre de l'annonce
        description = []
        extract_description = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "id-desc-body")]/text()').extract()
        if extract_description:
            description += extract_description

        redirect_description = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "id-desc-body")]//@href').extract()
        if  redirect_description:
            description.append(redirect_description[0])
        i.add_value(
            "description",
            description,
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/*[@class='id-price']/strong/text()")
        area = response.xpath(f'{ROOT_XPATH}/*[contains(text(), "Surface habitable")]/following-sibling::dd/text()').extract()
        i.add_value("area", " ".join(area[:2]) if area else "")

        land = response.xpath(f'{ROOT_XPATH}/*[contains(text(), "Surface terrain")]/following-sibling::dd/text()').extract()
        i.add_value("land_surface", " ".join(land[:2]) if land else "")

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[contains(text(), 'Pièces')]/following-sibling::dd/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[contains(text(), 'Chambres')]/following-sibling::dd/text()")


        location = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "id-title-location")]/text()').extract()
        if location:
            location = location[0].strip().replace("\xa0", "")
        i.add_value("city", location.split('(')[0])
        try:
            i.add_value("postal_code", location.split('(')[1][:-1])
        except:
            logging.debug('Error while extracting postal_code for immonot')


        i.add_value("agency", True)
        i.add_value("agency_name", "Immonot")

        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@id, 'gallery')]//img[contains(@class, 'id-gallery-thumbs')]/@src")

        others = []

        letter_diagnostic = response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'i-gauge-current')]/text()").extract()
        chiffre_diagnostic = response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'i-gauge-value')]/text()").extract()
       
        count = 0
        for v in letter_diagnostic:
            if count == 0:
                others.append(" ".join(["DPE", letter_diagnostic[count], chiffre_diagnostic[count]])) 
            else:
                 others.append(" ".join(["GES", letter_diagnostic[count], chiffre_diagnostic[count]]))
            count += 1

        elems = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "id-spec")]')[:-1]
        for elem in elems:
            value = " ".join([cell for cell in elem.xpath('.//text()').extract() if cell and cell.strip()]).strip()
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
        return url_cleaned.split("/")[-2].split('__')[-1]