# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class WwwDytt8NetItem(scrapy.Item):
    # define the fields for your item here like:
    collection_name = scrapy.Field()
    title = scrapy.Field()
    publish_time = scrapy.Field()
    # images = scrapy.Field()
    # download_links = scrapy.Field()
    # contents = scrapy.Field()
