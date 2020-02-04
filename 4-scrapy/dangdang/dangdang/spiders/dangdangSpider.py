# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree
from ..items import DangdangItem

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['dangdang.com']
    redis_key = 'dangdang:start_urls'
    start_urls = ['http://category.dangdang.com/cp01.41.70.01.03.00-as8589934592%3A8589934823.html']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                    Safari/537.36 SE 2.X MetaSr 1.0'
    }

    base_url = 'http://category.dangdang.com'

    def get_class_span(self, url):
        response = etree.HTML(requests.get(url=(self.base_url + url), headers=self.headers).content.decode('GBK'))
        categorys = response.xpath('//li[@dd_name="分类"]/div[@class="list_right"][1]//div[@class="clearfix"]/span')
        return categorys

    def start_requests(self):
        categorys_1 = self.get_class_span('/cp01.00.00.00.00.00.html')
        for item in categorys_1:
            categorys_2 = self.get_class_span(item.xpath('a/@href').pop())
            for i in categorys_2:
                categorys_3 = self.get_class_span(i.xpath('a/@href').pop())
                for j in categorys_3:
                    categorys_4 = self.get_class_span(j.xpath('a/@href').pop())
                    for k in categorys_4:
                        self.start_urls.append('http://category.dangdang.com' + k.xpath('a/@href').pop())
        print(self.start_urls)
        yield scrapy.Request(url=self.start_urls, headers=self.headers, method='GET', callback=self.parse)

    def parse(self, response):
        list = response.xpath('//ul[@id="component_59"]/li')
        for li in list:
            try:
                item = DangdangItem()
                item['collection_name'] = 'detail'
                item['cover_url'] = li.xpath('a[1]/img/@data-original').extract_first()
                if not item['cover_url']:
                    item['cover_url'] = li.xpath('a[1]/img/@src').extract_first()
                item['_id'] = li.xpath('@id').extract_first()
                item['title'] = li.xpath('a[1]/@title').extract_first().strip()
                item['detail'] = li.xpath('p[2]/text()').extract_first()
                item['price'] = li.xpath('p[3]/span[1]/text()').extract_first()
                author_time_press = li.xpath('p[@class="search_book_author"]')
                item['author'] = author_time_press.xpath('span[1]/a/@title').extract_first()
                item['time'] = author_time_press.xpath('span[2]/text()').extract_first().strip().replace('/', '')
                item['press'] = author_time_press.xpath('span[3]/a/text()').extract_first()
                item['comment_num'] = li.xpath('p[@class="search_star_line"]/a[1]/text()').extract_first().strip().replace(u'条评论', '')
                yield item
            except Exception:
                print(item['_id'] + "解析错误")
                continue
        next_page = response.xpath('//div[@class="paging"]/ul/li[@class="next"]/a/@href').extract_first()
        # print(next_page)
        if next_page:
            yield scrapy.Request(url=self.base_url + next_page, headers=self.headers, callback=self.parse)