#!/usr/bin/env python3
# encoding=utf-8

import re
import json
import requests

if __name__ == "__main__":
    url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
    response = requests.get(url, verify=False)
    stations = re.findall(r'([A-Z]+)\|([a-z]+)', response.text)
    stations = dict(stations)
    stations = dict(zip(stations.values(), stations.keys()))      #将字典中的键值对反转

    ''' 把字典存储到文件stations.py '''
    ''' method 1 '''
    print('stations = ', stations)       #执行命令：python3 parse_station.py > stations.py

    ''' method 2 '''
    # with open('stations.py', 'w', encoding='utf-8') as f:    #使用文件操作存储
    #     f.write('stations = ')
    #     f.write(json.dumps(stations))