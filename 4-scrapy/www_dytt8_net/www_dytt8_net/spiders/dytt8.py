# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from www_dytt8_net.items import WwwDytt8NetItem

class Dytt8Spider(CrawlSpider):
    name = 'dytt8'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['http://www.dytt8.net/']

    rules = (
        # 追踪除游戏外的所有列表页
        Rule(LinkExtractor(deny=r'.*game.*', allow='.*/index\.html')),
        # 对下一页进行追踪
        Rule(LinkExtractor(restrict_xpaths=u'//a[text()="下一页"]')),
        # 对文章进行提取并回调给parse_item处理, 过滤掉游戏
        Rule(LinkExtractor(allow=r'.*/\d+/\d+\.html', deny=r".*game.*"), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = WwwDytt8NetItem()
        item['collection_name'] = 'dytt8'
        item['title'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract_first()
        item['publish_time'] = response.xpath('//div[@class="co_content8"]/ul/text()').extract_first().strip().replace('发布时间：', '')
        #下面的几个属性我没去写了，有需要的可以自己去试一下下面的能不能爬取
        # item['images'] = response.xpath('//div[@class="title_all"]/h1/font/text()').extract_first()
        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
        yield item
