# -*- coding: utf-8 -*-
BOT_NAME = 'fluximmo'

SPIDER_MODULES = ['fluximmo.spiders']
NEWSPIDER_MODULE = 'fluximmo.spiders'

ROBOTSTXT_OBEY = False
FEED_EXPORT_ENCODING = 'utf-8'

SPIDER_MIDDLEWARES = {
    "fluximmo.middlewares.metaPassthroughMiddleware.MetaPassthroughMiddleware": 100,
}