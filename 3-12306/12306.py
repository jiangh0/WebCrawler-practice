#!/usr/bin/env python3
# encoding=utf-8

'''
参考：https://zhuanlan.zhihu.com/p/23561159   https://www.jianshu.com/p/89f6170991c8
Train tickets query via command-line.

Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Example:
    tickets beijing shanghai 2016-08-25
'''

from docopt import docopt
# from prettytable import prettytable
from stations import stations
import requests
import json

def cli():
    ''' command-line interface '''
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    age = 'ADULT'
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(date, from_station, to_station, age)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }
    requests.packages.urllib3.disable_warnings() # 关闭https证书验证警告
    response = requests.get(url,headers=headers, verify=False)   #有时候返回error.html
    print(response.json())
    print(response.text)
    # print(response.json())
    print(json.loads(response.content))
    return json.dumps(response)

def deal_result(results):
    trains = []
    for item in results:
        item.split('|')
        train=0

    pass


if __name__ == '__main__':
    result = cli()
    print(result)