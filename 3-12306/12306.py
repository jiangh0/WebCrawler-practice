#!/usr/bin/env python3
# encoding=utf-8

'''
参考：https://zhuanlan.zhihu.com/p/22235740    https://www.jianshu.com/p/89f6170991c8
2020-2未完成
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
    # requests.packages.urllib3.disable_warnings() # 关闭https证书验证警告
    arguments = docopt(__doc__)
    from_station = stations.get(arguments['<from>'])
    to_station = stations.get(arguments['<to>'])
    date = arguments['<date>']
    age = 'ADULT'
    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}'.format(date, from_station, to_station, age)
    

    res = requests.get('https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=ZUE777PrMJ&hashCode=HTlCseMJ8pkxPVat099LN7HS7AcWyCZwITTx7_FFpGs&FMQw=0&q4f3=zh-CN&VySQ=FGGnO8THpiWIg4IgV1RK71Bg5Y11jb40&VPIf=1&custID=133&VEek=unknown&dzuS=0&yD16=0&EOQP=8f58b1186770646318a429cb33977d8c&jp76=52d67b2a5aa5e031084733d5006cc664&hAqN=Win32&platform=WEB&ks0Q=d22ca0b81584fbea62237b14bd04c866&TeRS=824x1536&tOHY=24xx864x1536&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(', 
        verify=False)
    a = res.content.split(b':')[2]
    RAIL_DEVICEID = a.split(b'\"')[1]
    headers = {
        # 'Cookie': 'tk=2FFogFazP393oAT7W7i9l1fUug7jTn2kcHh63Qy0j1j0; JSESSIONID=8AF47A56D7F0031030EFC01FE55C9C42; BIGipServerpassport=1005060362.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2020-02-12; _jc_save_toDate=2020-02-01; RAIL_EXPIRATION=1580858133009; RAIL_DEVICEID={}; BIGipServerpool_passport=216859146.50215.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u6210%u90FD%2CCDW; BIGipServerotn=1389953290.24610.0000'.format(RAIL_DEVICEID),
        # 'Cookie': 'RAIL_DEVICEID={}; _jc_save_toStation=%u6210%u90FD%2CCDW'.format(RAIL_DEVICEID),
        'Cookie': 'tk=2FFogFazP393oAT7W7i9l1fUug7jTn2kcHh63Qy0j1j0; JSESSIONID=8AF47A56D7F0031030EFC01FE55C9C42; BIGipServerpassport=1005060362.50215.0000; route=9036359bb8a8a461c164a04f8f50b252; _jc_save_wfdc_flag=dc; _jc_save_fromDate=2020-02-12; _jc_save_toDate=2020-02-01; RAIL_EXPIRATION=1580858133009; RAIL_DEVICEID=a9Ew9ov2WrMlbQSg-FmjUWdcH3ZAwHnhe7pVOAgAKf7xTWBJbx_-eIvBi7FpiDtMmhY3V3uSjeHcUX9-1h1nHIFZv2g1Y_6Os1MHxSy7--LyRk_bYJA2v54wWZ5B96jNGfdB_0BmEsSbT6by_rbzxLWoY3MXONCr; BIGipServerpool_passport=216859146.50215.0000; _jc_save_fromStation=%u5317%u4EAC%2CBJP; _jc_save_toStation=%u6210%u90FD%2CCDW; BIGipServerportal=3134456074.17183.0000; BIGipServerotn=317719050.24610.0000',
        'Referer': 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.get(url, headers=headers, verify=False)   #有时候返回error.html
    print(response.content)
    return json.dumps(response)

def deal_result(results):
    trains = []
    for item in results['data']['result']:
        print(item)
        item.split('|')

    pass


if __name__ == '__main__':
    results = cli()
    deal_result(results)