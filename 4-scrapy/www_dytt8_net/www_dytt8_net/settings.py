# -*- coding: utf-8 -*-

# Scrapy settings for www_dytt8_net project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'www_dytt8_net'

SPIDER_MODULES = ['www_dytt8_net.spiders']
NEWSPIDER_MODULE = 'www_dytt8_net.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'www_dytt8_net.pipelines.WwwDytt8NetPipeline': 300
}

MONGODB_HOST = '127.0.0.1'
MONGODB_PORT = 27017
MONGODB_DBNAME = "spider_world"