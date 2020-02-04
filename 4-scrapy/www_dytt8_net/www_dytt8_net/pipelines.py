# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import json
import codecs

class WwwDytt8NetPipeline(object):
    def __init__(self, db_name, host, port):
        self.db_name = db_name
        self.host = host
        self.port = port

    # def process_item(self, item, spider):
    #     '''先判断itme类型，在放入相应数据库'''
    #     # if isinstance(item, WwwDytt8NetItem):
    #     #     try:
    #     #         info = dict(item)
    #     #         self.post.insert(info)
    #     #     except Exception:
    #     #         pass
    #     return item

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_name=crawler.settings.get('MONGODB_DBNAME'),
            host=crawler.settings.get('MONGODB_HOST'),
            port=crawler.settings.get('MONGODB_PORT')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(host=self.host, port=self.port)
        self.db = self.client[self.db_name]

    def process_item(self, item, spider):
        self.db[item['collection_name']].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()