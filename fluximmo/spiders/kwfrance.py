# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.kwfrance import KwFrance
import pdb

logger = logging.getLogger(__name__)


class KwFranceSpider(CrawlSpiderFluximmo):
    name = "kwfrance"  # nom du portail
    allowed_domains = ["kwfrance.com"]  # Domaine(s) du portail
    website = "kwfrance.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(KwFranceSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/kwfrance\.com\/property\/([0-9]*)",
        )

    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        return [
            'https://kwfrance.com/result/index?view_type=list&btn_votre_projet_text=Achat+-+Appartement+%28%2B5%29&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Btransaction_ides%5D%5B%5D=1&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=1&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=2&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=4&PropertieSearch%5Bprogramme&page={page_index}&per-page=12',
            'https://kwfrance.com/result/index?view_type=list&btn_votre_projet_text=Location+-+Appartement+%28%2B5%29&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Btransaction_ides%5D%5B%5D=1&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=1&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=2&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=4&PropertieSearch%5Bprogramme&page={page_index}&per-page=12',
        ]

    def parse_item(self, response):
        logger.debug(f'parse_item --------------> {response.url}')
        i = ItemLoader(item=KwFrance(), response=response)
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
            f'{ROOT_XPATH}/*[contains(@class, "about__desc")]/text()',
        ) # Description de l'annonce
        

        i.add_xpath("price", f"{ROOT_XPATH}/*[contains(@class, 'header')]//*[contains(@class, 'price')]/text()")
        i.add_xpath("area", f'{ROOT_XPATH}/*[@class="result-info__item"]/*[contains(text(), " m")]/text()[1]')

        i.add_xpath("land_surface", f'{ROOT_XPATH}/*[contains(text(), "Surface")]/following-sibling::div/text()')

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[@class='result-info__item']/*[contains(text(), ' pièces')]/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[@class='result-info__item']/*[contains(text(), ' chambres')]/text()")

        i.add_xpath("postal_code", f"{ROOT_XPATH}/*[contains(@id, 'postal-code')]/@value")
        i.add_xpath("city", f"{ROOT_XPATH}/*[contains(@class, 'column--title')]/text()")

        i.add_value("agency", True)
        i.add_value("agency_name", "Kwfrance")

        photos = response.xpath(f"{ROOT_XPATH}/img[contains(@class, 'gallery')]/@src").extract()
        photo_clean = []
        for photo in photos:
            if "kwfrance.com" not in photo:
                photo_clean.append("https://kwfrance.com" + photo)
            else:
                photo_clean.append(photo)
        i.add_value("photos", photo_clean)

        others = []
        
        letter_diagnostic = response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'active view-diagnostic')]//*[contains(@class, 'value-number')]/text()").extract()
        chiffre_diagnostic = response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'active view-diagnostic')]//*[contains(@class, 'name')]/text()").extract()
        if not chiffre_diagnostic:
            chiffre_diagnostic = response.xpath("//*[contains(@class, 'diagnostic__table-item--active')]//*[contains(@class, 'properties__value')]/text()").extract()
            letter_diagnostic = response.xpath("//*[contains(@class, 'diagnostic__table-item--active')]/div[1]/text()").extract()

        count = 0
        for v in chiffre_diagnostic:
            if count == 0:
                others.append(" ".join(["DPE", letter_diagnostic[count], v])) 
            else:
                 others.append(" ".join(["GES", letter_diagnostic[count], v]))
            count += 1

        elems = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "details-list")]/li')
        for elem in elems:
            value = "".join([cell for cell in elem.xpath('.//text()').extract() if cell]).strip()
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