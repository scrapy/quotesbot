# -*- coding: utf-8 -*-
import logging

from .crawl_spider import CrawlSpiderFluximmo
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from ..url_utils import clean_url
from ..items.annonce import Annonce
import pdb

logger = logging.getLogger(__name__)


class GoodShowCaseSpider(CrawlSpiderFluximmo):
    name = "goodshowcase"  # nom du portail
    allowed_domains = ["www.goodshowcase.com"]  # Domaine(s) du portail
    website = "www.goodshowcase.com"  # domaine principal

    def __init__(self, *args, **kwargs):
        super(GoodShowCaseSpider, self).__init__(*args, **kwargs)

        """Regex décrivant les formats possibles pouvant prendre les URLs d'une annonce spécifique"""
        self.link_extractor_annonces = LinkExtractor(
            allow=r"https:\/\/www\.goodshowcase\.com\/annonce-([a-zA-Z-0-9]*).html",
        )

    """Génération statique ou dynamique des URLs de listing à scraper (page 1)"""
    def generate_all_urls(self):
        # TODO quand les 6 sont en meme temps, sa fail, retour 400 mais quand on en mets que 2 et le reste en commentaire, sa fonctionne, 
        # il faudrait faire un petit changement dans la spider parent pour permettre plusieur call a generate_all_urls
        return [
            'https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=louer&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=84&id_region%5B%5D=27&id_region%5B%5D=53&id_region%5B%5D=94&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page={page_index}'
            'https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=acheter&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=84&id_region%5B%5D=27&id_region%5B%5D=94&id_region%5B%5D=53&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page={page_index}'

            'https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=louer&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=44&id_region%5B%5D=32&id_region%5B%5D=11&id_region%5B%5D=28&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page={page_index}'
            'https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=acheter&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=44&id_region%5B%5D=32&id_region%5B%5D=11&id_region%5B%5D=28&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page={page_index}'

            'https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=louer&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=75&id_region%5B%5D=76&id_region%5B%5D=52&id_region%5B%5D=93&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page={page_index}'
            'https://www.goodshowcase.com/index.php?mod=search&url_transaction%5B%5D=acheter&url_bien%5B%5D=appartement&url_bien%5B%5D=maison&url_bien%5B%5D=terrain&url_bien%5B%5D=local&url_bien%5B%5D=stationnement&id_agence=&id_region%5B%5D=75&id_region%5B%5D=76&id_region%5B%5D=52&id_region%5B%5D=93&id_dept%5B%5D=&cp=&distance=0&distroute=0&tmpsroute=0&surfmin=&surfmax=&sejmin=&sejmax=&cuisine=&chauffage=&sdbmin=&sdbmax=&sdemin=&sdemax=&wcmin=&wcmax=&etagemin=&etagemax=&ascenseur=&balcon=&bbc=&box=&calme=&cave=&cheminee=&climatisation=&dernier_etage=&digicode=&gardien=&interphone=&parking=&parquet=&piscine=&meuble=&refait_a_neuf=&terrasse=&vue_degagee=&terrmin=&terrmax=&prixmin=&prixmax=&piecemin=&piecemax=&chambremin=&chambremax=&constructmin=&constructmax=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&motcle%5B%5D=&visavis=&affph=&affmr=&affme=&dataj=1&page=1&carte=&ordre=ajout&page={page_index}'
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

        i.add_xpath("title", f'{ROOT_XPATH}/*[contains(@class, "row")]//*[contains(@id, "carousel-text")]/h2/text()') # Titre de l'annonce
        i.add_xpath(
            "description",
            f'{ROOT_XPATH}/*[contains(@class, "row")]//*[contains(@id, "carousel-text")]/*[contains(@class, "text")]/text()',
        ) # Description de l'annonce

        i.add_xpath("price", f"{ROOT_XPATH}/h1/div[2]/text()")
        i.add_xpath("area", f'{ROOT_XPATH}/*[contains(text(), "Surface")]/../following-sibling::div/text()')

        i.add_xpath("land_surface", f'{ROOT_XPATH}/*[contains(text(), "Terrain")]/../following-sibling::div/text()')

        i.add_xpath("rooms", f"{ROOT_XPATH}/*[contains(text(), 'Pièces')]/../following-sibling::div/text()")
        i.add_xpath("bedrooms", f"{ROOT_XPATH}/*[contains(text(), 'Chambres')]/../following-sibling::div/text()")


        i.add_xpath("postal_code", f"{ROOT_XPATH}/*[contains(@class, 'row')]//*[contains(@id, 'carousel-text')]/h3/text()")
        city = response.xpath("//*[contains(@class, 'row')]//*[contains(@id, 'carousel-text')]/h3/text()").extract()
        i.add_value("city", city[0][:-5].strip())


        i.add_value("agency", True)
        i.add_value("agency_name", "Goodshowcase")

        i.add_xpath("photos",f"{ROOT_XPATH}/*[contains(@class, 'thumbnail')]/img/@src")

        others = []
        try:
            others.append("DPE " + response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'row')]//*[contains(@id, 'carousel-text')]//*[contains(@id, 'dpe')]//*[contains(@class, 'arrow')]/text()").extract_first())
        except:pass
        try:
            others.append("GES " + response.xpath(f"{ROOT_XPATH}/*[contains(@class, 'row')]//*[contains(@id, 'carousel-text')]//*[contains(@id, 'ges')]//*[contains(@class, 'arrow')]/text()").extract_first())
        except:pass

        
        elems = response.xpath(f'{ROOT_XPATH}/*[contains(@class, "row")]//*[contains(@id, "carousel-text")]/*[contains(@class, "row")][1]/div')
        for elem in elems:
            value = " ".join([cell for cell in elem.xpath('.//text()').extract() if cell]).strip()
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
        return url_cleaned.split("-")[-1].split(".")[0]