# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import requests
import os

class DangdangPipeline(object):
    def __init__(self, db_name, host, port):
        self.db_name = db_name
        self.host = host
        self.port = port

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
        #存入数据库
        self.db[item['collection_name']].insert(dict(item))
        #存储图片
        if not os.path.exists('./images'):
            os.makedirs('./images')
        if item['cover_url']:
            path = './images/' + item['_id'] + '.jpg'
            with open(path, 'wb') as f:
                image = requests.get(item['cover_url'])
                f.write(image.content)
        return item

    def close_spider(self, spider):
        self.client.close()
