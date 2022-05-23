# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.engelvoelkers import Engelvoelkers
from scrapy import Request
from datetime import datetime
import pdb


logger = logging.getLogger(__name__)


class engelvoelkersSpider(CrawlSpiderFluximmo):
    name = "engelvoelkers"  # nom du portail
    allowed_domains = ["www.engelvoelkers.com"]  # Domaine(s) du portail
    website = "www.engelvoelkers.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(engelvoelkersSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.engelvoelkers\.com\/fr-fr\/bien-immobilier\/([a-zA-Z-0-9.]*)_exp\/",
        )

    def start_crawler_list(
            self, stock=False, max_pages=1, rent_or_buy="both", ile_de_france="all"
    ):
        max_pages = self.MAX_PAGES
        PAGE_INDEX = 0

        for url in self.generate_all_urls():
            url_unformated = url
            url_formated = url.format(page_index=PAGE_INDEX)

            request = Request(url=url_formated, callback=self.parse_list, priority=10)

            request.meta["page_index"] = PAGE_INDEX
            request.meta["page_url"] = url_formated
            request.meta["page_url_unformated"] = url_unformated
            request.meta["stock"] = stock
            request.meta["max_pages"] = max_pages
            request.meta["pages_without_new_ads"] = 0
            request.meta["spider_type"] = self.name
            request.meta["max_pages"] = max_pages
            request.meta["date"] = datetime.now()
            request.meta["retry_times"] = 0
            request.meta["origin"] = {
                "spider": self.name,
                "added_from": "SCRAPY",
                "ref": url_formated,
                "departement": None,
                "offer_type": None,
                "page_index": PAGE_INDEX,
                "date": datetime.now(),
            }

            yield request

    def next_list_page(self, response, pages_without_new_ads=-1):
        page_index = response.meta['page_index']
        max_pages = response.meta['max_pages']
        pages_without_new_ads = response.meta['pages_without_new_ads']
        page_url_unformated = response.meta['page_url_unformated']

        if page_index >= max_pages or pages_without_new_ads >= self.MAX_PAGES_WITHOUT_NEW_ADS:
            logger.debug(f"Stop next_list_page {response.url}")
            return None

        page_url_formated = page_url_unformated.format(page_index=page_index + 16)

        request = Request(
            page_url_formated,
            callback=self.parse_list,
            priority=max(100 - page_index, 10),
        )
        request.meta["page_index"] = page_index + 16
        request.meta["retry_times"] = 0
        request.meta["pages_without_new_ads"] = pages_without_new_ads
        request.meta["page_url"] = page_url_formated
        request.meta["page_url_unformated"] = page_url_unformated
        request.meta["stock"] = None
        request.meta["max_pages"] = max_pages
        request.meta["spider_type"] = self.name
        request.meta["date"] = datetime.now()
        request.meta["retry_times"] = 0
        request.meta["origin"] = {
            "spider": self.name,
            "added_from": "SCRAPY",
            "ref": page_url_formated,
            "departement": None,
            "offer_type": None,
            "page_index": page_index + 16,
            "date": datetime.now(),
        }
        logger.debug(f"Check next_list_page {page_index + 16} => {page_url_formated}")
        return request

    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            'https://www.engelvoelkers.com/fr/search/?q=&startIndex={page_index}&businessArea=residential&sortOrder=DESC&sortField=newestProfileCreationTimestamp&pageSize=18&facets=bsnssr%3Aresidential%3Bcntry%3Afrance%3B'
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')
        i = ItemLoader(item=Engelvoelkers(), response=response)
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
            f'{ROOT_XPATH}/*[contains(@class, "ev-exposee-text")]/text()',
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/*[@itemprop='price']/text()")
        i.add_xpath("area", f'{ROOT_XPATH}/*[contains(text(), "Surface Habitable")]/preceding-sibling::div/text()')

        i.add_xpath("land_surface", f'{ROOT_XPATH}/*[contains(text(), "terrain")]/preceding-sibling::div/text()')

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[contains(text(), 'Pièces')]/../following-sibling::div/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[contains(text(), 'Chambres')]/../following-sibling::div/text()")

        # no postal code
        i.add_value("postal_code", "") 
        city = response.xpath(f"{ROOT_XPATH}/h1/following-sibling::div/text()").extract()
        i.add_value("city", city[0].split(", ")[-1] if city else "")
            


        i.add_value("agency", True)
        i.add_value("agency_name", "Engelvoelkers")

        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@class, 'image-link')]/@href")

        # TODO mettre dans others toute les caractéristique + dpe ges
        others = []

        elems = response.xpath(f'{ROOT_XPATH}/ul[contains(@class, "exposee-detail-facts")]//li')
        for elem in elems:
            value = "".join([cell for cell in elem.xpath('.//text()').extract() if cell]).strip().replace(':', ' ')
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
        return url_cleaned.split("-")[-1].split("_")[0]