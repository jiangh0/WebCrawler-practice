#!/usr/bin/env python3
# encoding=utf-8

'''
参考：https://blog.csdn.net/ITBigGod/article/details/103123683
2020.1完结
'''

import requests
import codecs
import json
import csv

def download_page(num):
    url = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=" + str(num) + "&page_start=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    return requests.get(url, headers=headers).text
    
def deal_json(result_json):
    if result_json:
        return json.loads(result_json)
    return None

def output_csv(data):
    with open('movies.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['序号', '名字', '评分', '封面图片'])
        i = 1
        for item in data['subjects']:
            writer.writerow([i, item['title'], item['rate'], item['cover']])
            i += 1


if __name__ == "__main__":
    result_json = download_page(100)   #参数：需要抓取的数量
    result = deal_json(result_json)
    output_csv(result)