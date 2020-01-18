#!/usr/bin/env python3
# encoding=utf-8

'''
参考：https://cuiqingcai.com/2599.html   http://cuiqingcai.com/912.html
2020-1
'''

import csv
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


TIMEOUT = 20

def get_link_list(url, keyword, link_num, driver):
    driver.get(url)
    element = driver.find_element_by_name('q')
    for word in keyword:
        element.send_keys(word + ' ')
    element.send_keys(Keys.RETURN)

    # lists = driver.find_elements_by_xpath("//div[@id=J_ItemList]/div")
    # for item in lists:
    #     print(item.find_elements_by_xpath("/p[@class=productTitle]/a"))

    # try:
    #     element = WebDriverWait(driver, 10).until(
    #         EC.presence_of_element_located((By.ID, "J_TabBarBox"))
    #     )
    # finally:
    #     driver.quit()
    link_list = []
    for i in range(link_num):
        html = driver.page_source
        try:
            js = "window.scrollTo(0, document.body.scrollHeight - 1200)"
            driver.execute_script(js)
        except Exception:
            print(u'页面下拉失败')
        link_list[-1: -1] = parse_html(html)
        try:
            next_button = driver.find_element_by_css_selector('#content b.ui-page-num > a.ui-page-next')
            next_button.click()
        except Exception:
            print(u'没找到翻页按钮，结束')
            break
    return link_list

def parse_html(html):
    ''' 解析搜索结果页，获取所有商品链接 '''
    soup = BeautifulSoup(html)
    products = soup.find_all('div', attrs={'class': 'product'})
    links = []
    for product in products:
        link = product.find('p', attrs={'class': 'productTitle'})
        links.append('https:' + link.a['href'])
    return links
    
def get_product_detail(link_list, driver):
    ''' 根据商品链接爬取评价，保存到csv文件 '''
    for i, link in enumerate(link_list):
        driver.get(link)
        driver.execute_script("document.getElementsByClassName('sufei-dialog')[0].style.display='none'")  #未登录情况下关闭弹窗

        title = driver.find_element_by_css_selector('#J_DetailMeta h1').text    #获取商品名称
        driver.execute_script("window.scrollTo(0, 600)")
        try:
            WebDriverWait(driver, TIMEOUT).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#J_TabBar>li"))
            )
            driver.find_elements_by_css_selector('#J_TabBar>li')[1].find_element_by_css_selector('a').click()
        except Exception:
            print(u'加载超时')
        while True:
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight-" + str(count * count* 200) + ")")
            soup = BeautifulSoup(driver.page_source, features='html.parser')
            trs = soup.find(attrs={'id': 'J_Reviews'}).find_all('tr')
            reviews = []
            for tr in trs:
                size_and_color = tr.find('div', attrs={'class': 'rate-sku'}).find_all('p')
                review = [re.sub('[<span> | </span>]', '', tr.find('div', attrs={'class': 'rate-user-info'}).getTetxt()), size_and_color[0]['title'].split(':')[1], size_and_color[1]['title'].split(':')[1], tr.find('div', attrs={'class': 'tm-rate-fulltxt'}).getText()]
                print(review)
                reviews.append(review)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight-3000)")
            # try: 
            #     driver.find_elements_by_css_selector('#J_Reviews div.rate-paginator a')[2].click()  #下一页按钮点击
            #     break
            # except Exception:
            #     print(u'最后一页了')
            break
        with open('./products/{}{}{}.csv'.format(str(i+1), '--', title), mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['昵称', '主要颜色', '尺码', '评价'])
            print(reviews)
            for review in reviews:
                writer.writerow(review)

def login():
    pass

if __name__ == "__main__":
    # driver = webdriver.Chrome(r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe') #windows chrome驱动插件放置在相应目录
    driver = webdriver.Chrome()   #mac chrome驱动插件放在/usr/local/bin
    url = 'https://www.tmall.com/'
    login()
    link_list = get_link_list(url, ['优衣库', '牛仔裤'], 10, driver)
    get_product_detail(link_list, driver)
    driver.quit()
