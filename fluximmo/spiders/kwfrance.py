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
            'https://kwfrance.com/result/index?view_type=list&btn_votre_projet_text=Achat+-+Appartement+(%2B5)&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Btransaction_ides%5D%5B%5D=1&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=1&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bpropx_typeides%5D%5B%5D=2&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=4&PropertieSearch%5Bprogramme_neuf%5D=0&PropertieSearch%5Bprestige%5D=0&PropertieSearch%5Bprestige%5D=1&PropertieSearch%5Bbail_type%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=6&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=3&PropertieSearch%5Bautres%5D=0&PropertieSearch%5Bdepartments%5D%5B%5D=Var&PropertieSearch%5Bdepartment_codes%5D%5B%5D=83&btn_budget_text=Budget&PropertieSearch%5Bprix_min%5D=&PropertieSearch%5Bprix_max%5D=&btn_piece_text=Pi%C3%A8ces&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&btn_surface_text=Surface&PropertieSearch%5Bsurface_global_min%5D=&PropertieSearch%5Bsurface_global_max%5D=&PropertieSearch%5Bsurface_terrain_min%5D=&PropertieSearch%5Bsurface_terrain_max%5D=&PropertieSearch%5Bsort%5D=date_desc&PropertieSearch%5Bancien%5D=0&PropertieSearch%5Bneuf%5D=0&PropertieSearch%5Bvia_viager%5D=0&PropertieSearch%5Bprog_neuf%5D=0&PropertieSearch%5Brez_chaussee%5D=0&PropertieSearch%5Brez_jardin%5D=0&PropertieSearch%5Bdernier_etage%5D=0&PropertieSearch%5Bbordmer%5D=0&PropertieSearch%5Bpiscine%5D=0&PropertieSearch%5Bmeuble%5D=0&PropertieSearch%5Bnbr_balcon%5D=0&PropertieSearch%5Bjardin%5D=0&PropertieSearch%5Btennis%5D=0&PropertieSearch%5Bcalme%5D=0&PropertieSearch%5Bsoussol%5D=0&PropertieSearch%5Bnbr_terrrasse%5D=0&PropertieSearch%5Bgardien%5D=0&PropertieSearch%5Bascenseur%5D=0&PropertieSearch%5Bgrenier%5D=0&PropertieSearch%5Betage%5D=0&PropertieSearch%5Bvuemer%5D=0&PropertieSearch%5Bcheminee%5D=0&PropertieSearch%5Bnbr_cave%5D=0&PropertieSearch%5Bnbr_garage%5D=0&PropertieSearch%5Bacces_handicapes%5D=0&PropertieSearch%5Balarme%5D=0&PropertieSearch%5Bdigicode%5D=0&PropertieSearch%5Badsl_fibreoptique%5D=0&PropertieSearch%5Bnbr_wc%5D=0&PropertieSearch%5Bnbr_sdb%5D=0&PropertieSearch%5Bsejour_double%5D=0&PropertieSearch%5Bslc_cuisine%5D=0&PropertieSearch%5Bslc_typechauffage_collectif%5D=0&PropertieSearch%5Bslc_typechauffage_individuel%5D=0&PropertieSearch%5Bslc_typechauffage_mixte%5D=0&PropertieSearch%5Bmode_chauffage_gaz%5D=0&PropertieSearch%5Bmode_chauffage_electrique%5D=0&PropertieSearch%5Bmode_chauffage_fuel%5D=0&PropertieSearch%5Bmode_chauffage_autre%5D=0&PropertieSearch%5Bmode_chauffage_sol%5D=0&PropertieSearch%5Bmeca_chauffage_radiateur%5D=0&PropertieSearch%5Bmeca_chauffage_convecteurs%5D=0&PropertieSearch%5Bexposition_sejour_nord%5D=0&PropertieSearch%5Bexposition_sejour_sud%5D=0&PropertieSearch%5Bexposition_sejour_est%5D=0&PropertieSearch%5Bexposition_sejour_ouest%5D=0&PropertieSearch%5Bprop_url_visite_virtuelle%5D=0&PropertieSearch%5BLienVideo%5D=0&PropertieSearch%5Btypemandat_id%5D=0%5D(https://kwfrance.com/result/index?view_type=list&btn_votre_projet_text=Achat+-+Appartement+%28%2B5%29&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Btransaction_ides%5D%5B%5D=1&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=1&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=2&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=4&PropertieSearch%5Bprogramme&page={page_index}&per-page=12',
            'https://kwfrance.com/result/index?view_type=list&btn_votre_projet_text=Location+-+Appartement+(%2B5)&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Btransaction_ides%5D%5B%5D=1&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=1&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bpropx_typeides%5D%5B%5D=2&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=4&PropertieSearch%5Bprogramme_neuf%5D=0&PropertieSearch%5Bprestige%5D=0&PropertieSearch%5Bprestige%5D=1&PropertieSearch%5Bbail_type%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=6&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=3&PropertieSearch%5Bautres%5D=0&PropertieSearch%5Bdepartments%5D%5B%5D=Var&PropertieSearch%5Bdepartment_codes%5D%5B%5D=83&btn_budget_text=Budget&PropertieSearch%5Bprix_min%5D=&PropertieSearch%5Bprix_max%5D=&btn_piece_text=Pi%C3%A8ces&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_piece%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&PropertieSearch%5Bnbr_chambre%5D%5B%5D=0&btn_surface_text=Surface&PropertieSearch%5Bsurface_global_min%5D=&PropertieSearch%5Bsurface_global_max%5D=&PropertieSearch%5Bsurface_terrain_min%5D=&PropertieSearch%5Bsurface_terrain_max%5D=&PropertieSearch%5Bsort%5D=date_desc&PropertieSearch%5Bancien%5D=0&PropertieSearch%5Bneuf%5D=0&PropertieSearch%5Bvia_viager%5D=0&PropertieSearch%5Bprog_neuf%5D=0&PropertieSearch%5Brez_chaussee%5D=0&PropertieSearch%5Brez_jardin%5D=0&PropertieSearch%5Bdernier_etage%5D=0&PropertieSearch%5Bbordmer%5D=0&PropertieSearch%5Bpiscine%5D=0&PropertieSearch%5Bmeuble%5D=0&PropertieSearch%5Bnbr_balcon%5D=0&PropertieSearch%5Bjardin%5D=0&PropertieSearch%5Btennis%5D=0&PropertieSearch%5Bcalme%5D=0&PropertieSearch%5Bsoussol%5D=0&PropertieSearch%5Bnbr_terrrasse%5D=0&PropertieSearch%5Bgardien%5D=0&PropertieSearch%5Bascenseur%5D=0&PropertieSearch%5Bgrenier%5D=0&PropertieSearch%5Betage%5D=0&PropertieSearch%5Bvuemer%5D=0&PropertieSearch%5Bcheminee%5D=0&PropertieSearch%5Bnbr_cave%5D=0&PropertieSearch%5Bnbr_garage%5D=0&PropertieSearch%5Bacces_handicapes%5D=0&PropertieSearch%5Balarme%5D=0&PropertieSearch%5Bdigicode%5D=0&PropertieSearch%5Badsl_fibreoptique%5D=0&PropertieSearch%5Bnbr_wc%5D=0&PropertieSearch%5Bnbr_sdb%5D=0&PropertieSearch%5Bsejour_double%5D=0&PropertieSearch%5Bslc_cuisine%5D=0&PropertieSearch%5Bslc_typechauffage_collectif%5D=0&PropertieSearch%5Bslc_typechauffage_individuel%5D=0&PropertieSearch%5Bslc_typechauffage_mixte%5D=0&PropertieSearch%5Bmode_chauffage_gaz%5D=0&PropertieSearch%5Bmode_chauffage_electrique%5D=0&PropertieSearch%5Bmode_chauffage_fuel%5D=0&PropertieSearch%5Bmode_chauffage_autre%5D=0&PropertieSearch%5Bmode_chauffage_sol%5D=0&PropertieSearch%5Bmeca_chauffage_radiateur%5D=0&PropertieSearch%5Bmeca_chauffage_convecteurs%5D=0&PropertieSearch%5Bexposition_sejour_nord%5D=0&PropertieSearch%5Bexposition_sejour_sud%5D=0&PropertieSearch%5Bexposition_sejour_est%5D=0&PropertieSearch%5Bexposition_sejour_ouest%5D=0&PropertieSearch%5Bprop_url_visite_virtuelle%5D=0&PropertieSearch%5BLienVideo%5D=0&PropertieSearch%5Btypemandat_id%5D=0%5D(https://kwfrance.com/result/index?view_type=list&btn_votre_projet_text=Location+-+Appartement+%28%2B5%29&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Btransaction_ides%5D%5B%5D=1&PropertieSearch%5Btransaction_ides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=1&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=2&PropertieSearch%5Bprop_typeides%5D%5B%5D=0&PropertieSearch%5Bprop_typeides%5D%5B%5D=4&PropertieSearch%5Bprogramme&page={page_index}&per-page=12',
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

        i.add_xpath("photos",f"{ROOT_XPATH}/img[contains(@class, 'gallery')]/@src")

        others = []
        
        letter_diagnostic = response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'active view-diagnostic')]//*[contains(@class, 'value-number')]/text()").extract()
        chiffre_diagnostic = response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'active view-diagnostic')]//*[contains(@class, 'name')]/text()").extract()
       
        count = 0
        for v in letter_diagnostic:
            if count == 0:
                others.append(" ".join(["DPE", letter_diagnostic[count], chiffre_diagnostic[count]])) 
            else:
                 others.append(" ".join(["GES", letter_diagnostic[count], chiffre_diagnostic[count]]))
            count += 1

        elems = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "details-list")]/li')
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