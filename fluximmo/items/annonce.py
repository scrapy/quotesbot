# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import logging
import re
import unicodedata

import scrapy
from scrapy.loader.processors import Compose, Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

logger = logging.getLogger(__name__)


class Annonce(scrapy.Item):
    def __repr__(self):
        """only print out url after exiting the Pipeline"""
        return repr({"url": self["url"]})

    def find_postal_code(text):
        try:
            regex = r".*([0-9]{5}).*"

            matches = re.finditer(regex, text, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                for groupNum in range(0, len(match.groups())):
                    return match.groups(groupNum)[0]
        except Exception:
            return None

    def find_number(text):
        try:
            text = text.replace(' ', '')

            regex = r"[0-9]+"
            matches = re.finditer(regex, text, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                return int(match.group())
        except Exception:
            return None

    def remove_null_characters(description):
        if type(description) == list:
            description = description[0]
        description = str(description).replace("\u0000", "").replace("\x00", "")
        return description

    def deduplicate_urls(urls):
        return list(set(urls))

    def clean_html(html):
        if isinstance(html, str):
            text = re.sub("<[^>]+?>", "", html)
            return re.sub("\s\s+", " ", text)
        else:
            return html

    def comma_spans(spans):
        return spans.replace("</span>", "</span>:", 1).replace("\xa0", " ")

    def convert_to_array(strings):
        if strings is None or len(strings) == 0:
            return None
        if type(strings[0]) == dict:
            return strings

        strings = [
            Annonce.clean_html(
                Annonce.comma_spans(s) if ":" not in s else s.replace("\xa0", " ")
            )
            for s in strings
        ]
        assets = {}

        for s in strings:
            s = s.split(":")

            if len(s) > 1 and (type(s[1]) is not str or len(s[1].strip()) > 0):
                assets[s[0].strip()] = s[1].strip()
            else:
                if assets.get("assets") is None:
                    assets["assets"] = []
                if s[0].strip() != '':
                    assets["assets"].append(s[0].strip())
        return assets

    def others_treatment(others):
        rslt = {}
        for idx, o in enumerate(others):
            if type(others[idx]) == str:
                string = others[idx].replace("\t", " ").replace("\n", "")
                string = "".join(
                    [
                        c
                        for i, c in enumerate(string)
                        if not (string[i - 1] == c and c == " ")
                    ]
                )  # Remove double spaces
                if string is not None and len(string) > 0:
                    if rslt.get("assets") is None:
                        rslt["assets"] = []
                    rslt["assets"].append(string)
            else:
                if others[idx][next(iter(others[idx]))] is not None and (
                    type(others[idx][next(iter(others[idx]))]) is not str
                    or len(others[idx][next(iter(others[idx]))]) > 0
                ):
                    rslt = {**rslt, **others[idx]}

        return rslt

    url = scrapy.Field(output_processor=TakeFirst())
    public_url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(
        input_processor=MapCompose(
            str.strip, lambda x: unicodedata.normalize("NFKD", x)
        ),
        output_processor=Join(" "),
    )
    price = scrapy.Field(
        input_processor=MapCompose(find_number),
        output_processor = TakeFirst()
    )
    published_at = scrapy.Field(
        output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, remove_null_characters),
        output_processor=Join("\n"),
    )

    others = scrapy.Field(
        input_processor=Compose(convert_to_array),
        output_processor=Compose(others_treatment),
    )

    area = scrapy.Field(
        input_processor=MapCompose(find_number),
        output_processor=TakeFirst()
    )
    property_type = scrapy.Field(
        output_processor=TakeFirst()
    )
    bedrooms = scrapy.Field(
        input_processor=MapCompose(find_number),
        output_processor=TakeFirst()
    )
    rooms = scrapy.Field(
        input_processor=MapCompose(find_number),
        output_processor=TakeFirst()
    )
    city = scrapy.Field(
        output_processor=TakeFirst()
    )
    postal_code = scrapy.Field(
        output_processor=Compose(TakeFirst(), find_postal_code)
    )
    photos = scrapy.Field(
        input_processor=Compose(),
        output_processor=Compose(deduplicate_urls),
    )
    is_available = scrapy.Field(output_processor=TakeFirst())
    agency = scrapy.Field(output_processor=TakeFirst())

    agency_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    website = scrapy.Field(
        output_processor=TakeFirst()
    )
    site_id = scrapy.Field(
        output_processor=TakeFirst()
    )
    ads_type = scrapy.Field(
        output_processor=TakeFirst()
    )
    origin = scrapy.Field(
        output_processor=TakeFirst()
    )
    land_surface = scrapy.Field(
        input_processor=MapCompose(find_number),
        output_processor=TakeFirst()
    )
