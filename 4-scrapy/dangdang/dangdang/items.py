# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DangdangItem(scrapy.Item):
    collection_name = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    press = scrapy.Field()  #出版社
    time = scrapy.Field()
    price = scrapy.Field()
    comment_num = scrapy.Field()
    detail = scrapy.Field()
    cover_url = scrapy.Field()
    # category1 = scrapy.Field()  # 种类(小)
    # category2 = scrapy.Field()  # 种类(大)
