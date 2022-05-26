# -*- coding: utf-8 -*-
BOT_NAME = 'fluximmo'

SPIDER_MODULES = ['fluximmo.spiders']
NEWSPIDER_MODULE = 'fluximmo.spiders'

ROBOTSTXT_OBEY = False
FEED_EXPORT_ENCODING = 'utf-8'

URLLENGTH_LIMIT = 10000
USER_AGENT = 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'

SPIDER_MIDDLEWARES = {
    "fluximmo.middlewares.metaPassthroughMiddleware.MetaPassthroughMiddleware": 100,
    "scrapy.spidermiddlewares.urllength": None
}

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    'fluximmo.middlewares.proxyMiddleware.ProxyMiddleware': 100,
}