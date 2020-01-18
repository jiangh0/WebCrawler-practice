#!/usr/bin/env python3
# encoding=utf-8

'''
参考：https://zhuanlan.zhihu.com/p/20423182
2020.1
'''

import codecs
import requests
from bs4 import BeautifulSoup

URL = "https://movie.douban.com/top250"

def download_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    return requests.get(url, headers=headers).content
    
def parse_html(html):
    soup = BeautifulSoup(html)
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    for movie in movie_list_soup.find_all('li'):
        name = movie.find('span', attrs={'class': 'title'}).getText()
        movie_name_list.append(name)
    next_page = soup.find('span', attrs={'class': 'next'}).find('a')

    if next_page:
        return movie_name_list, URL + next_page['href']
    return movie_name_list, None


if __name__ == "__main__":
    url = URL
    
    with codecs.open('E:\\movies', 'wb', encoding='utf-8') as fp:
        while url:
            html = download_page(url)
            movies, url = parse_html(html)
            fp.write(u'{movies}\n'.format(movies='\n'.join(movies)))

    ''' 文件读写 '''
    with codecs.open('E:\\movies', 'r') as f:
        print(f.read())