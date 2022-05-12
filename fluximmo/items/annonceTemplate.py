# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import logging
from fluximmo.items.annonce import Annonce

logger = logging.getLogger(__name__)

class AnnonceTemplate(Annonce):
    name = "template"