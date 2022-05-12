import logging

from scrapy.http import Request

log = logging.getLogger("scrapy")
logging.getLogger("scrapy").setLevel(logging.INFO)


class MetaPassthroughMiddleware(object):
    def process_spider_output(self, response, result, spider):
        """
        Since we encapsulate every information in each request,
        We need to make sure the meta data are passed.
        Ensures the meta data from the response is passed
        through in any Request's generated from the spider
        """
        for x in result:
            # only operate on requests
            if isinstance(x, Request):
                # pass along all known meta fields, only if
                # they were not already set in the spider's new request
                for key in list(response.meta.keys()):
                    if key not in x.meta:
                        x.meta[key] = response.meta[key]
            yield x
