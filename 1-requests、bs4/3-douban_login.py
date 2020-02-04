#!/usr/bin/env python3
# encoding=utf-8

'''
参考：https://zhuanlan.zhihu.com/p/20494731
2020.1完结
'''

import json
import requests
from bs4 import BeautifulSoup


''' name:账号 password：密码 remember：是否记住 '''
def login(name, password, remenber):
    session = requests.session()
    url = 'https://accounts.douban.com/j/mobile/login/basic'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    data = {
        'name': name,
        'password': password,
        'remenber': remenber
    }
    response = session.post(url, data, headers=headers).content
    uid = json.loads(response)['payload']['account_info']['uid']
    print(BeautifulSoup(session.get('https://www.douban.com/people/' + uid, headers=headers).content).find('div', attrs={'class': 'info'}).find('h1').getText())
    return session


if __name__ == "__main__":
    login('email', 'password', True)
