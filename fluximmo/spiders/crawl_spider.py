import logging

from scrapy import Request
from scrapy.spiders import CrawlSpider
from datetime import datetime

logger = logging.getLogger(__name__)

class CrawlSpiderFluximmo(CrawlSpider):
    handle_httpstatus_list = [410, 404]
    MAX_PAGES_WITHOUT_NEW_ADS = 2
    MAX_PAGES = 4

    def __init__(self, *args, **kwargs):
        super(CrawlSpiderFluximmo, self).__init__(*args, **kwargs)
        self.link_extractor_annonces = None
        self.Request = Request
        self.urls = []

    def start_requests(self):
        return self.start_crawler_list()

    @staticmethod
    def gen_request_url(url):
        return url

    def is_new_ad(self, url):
        return True

    def start_crawler_list(
            self, stock=False, max_pages=1, rent_or_buy="both", ile_de_france="all"
    ):
        max_pages = self.MAX_PAGES
        PAGE_INDEX = 1

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

        page_url_formated = page_url_unformated.format(page_index=page_index + 1)

        request = Request(
            page_url_formated,
            callback=self.parse_list,
            priority=max(100 - page_index, 10),
        )
        request.meta["page_index"] = page_index + 1
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
            "page_index": page_index + 1,
            "date": datetime.now(),
        }
        logger.debug(f"Check next_list_page {page_index + 1} => {page_url_formated}")
        return request

    def parse_list(self, response):
        COUNT_NEW_ADS = 0
        links_found = self.link_extractor_annonces.extract_links(response)

        for ad_url in links_found:
            COUNT_NEW_ADS += 1
            ad_url = ad_url.url

            if self.is_new_ad(ad_url):
                ad_request = self.Request(
                    ad_url,
                    callback=self.parse_item,
                    priority=1000,
                )

                ad_request.meta["ad"] = ad_url
                ad_request.meta["ad_url"] = ad_url

                yield ad_request

        if COUNT_NEW_ADS == 0:
            response.meta['pages_without_new_ads'] += 1

        yield self.next_list_page(response, response.meta['pages_without_new_ads'])

    @staticmethod
    def extract_site_id(url):
        raise NotImplementedError("extract_site_id() not implemented")

    def generate_all_urls(self):
        raise NotImplementedError("generate_all_urls() not implemented")

    def parse_item(self, response):
        raise NotImplementedError("parse_item() not implemented")

    def start_crawler_check(self, stock=False):
        raise NotImplementedError("start_crawler_check() not implemented")

    def check_available(self, response):
        raise NotImplementedError("check_available() not implemented")
