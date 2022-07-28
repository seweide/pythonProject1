#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from selenium import webdriver
import time
import json as js
from lxml import etree
import math
import xlwt

def get_data(home_url, driver,data, category, keshi):

    url = home_url + category
    driver.get(url)
    time.sleep(0.2)
    sel = etree.HTML(driver.page_source)
    #药品标签

    #print(data)
    return data

def get_pageProps(home_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
    res = requests.get(home_url, headers=headers)
    sel = etree.HTML(res.content)
    script = sel.xpath('//body//script/text()')
    js_test = js.loads(script[0])
    pageProps = js_test['props']['pageProps']
    return pageProps

def login(home_url):
    chromedriver = "/Users/heweiwen/Downloads/work/Solf/chrome-mac/chromedriver"
    driver = webdriver.Chrome(executable_path=chromedriver)
    driver.get(home_url)  # 打开网址
    cookie1 = {"XSRF-TOKEN": "09e10e6d-ffed-41e8-9e5f-61668cbee132",
               "cookie2": "1726e5f82e9e47168a43445d1150720f","_tb_token_":"33f873f98173e"}
    cookie2 = {"sgcookie": "E100Bl5VNCulll2O9H0KCOOv5olQP3K%2Bgv1zoedw91zTcWjWsOkB4CA7uREjcQkkb8gjC6xzB%2F0yHtj%2BwmdHuVEL3qClwR2KZpSrKiAyp2fbTNk%3D",
               "cookie1": "VACLjwA8%2BDYj%2F4dg77pBdX8kMfs89QAdVEY5UmfdMe4%3D"}
    time.sleep(1)
    driver.add_cookie(cookie1)
    driver.add_cookie(cookie2)
    driver.get(home_url)
    time.sleep(1)
    return driver

def get_name(name):
    result = ""
    if str(len(name)) == '2':
        result = name[1]
    return result

# 获取成份的方法
def get_cf(drug_tag,info,name):
    result = ""
    for a in range(0, len(drug_tag)):
        type = drug_tag[a].xpath('./div[@class="cnName__3Kpx"]/text()')
        if type[1] == name:
            tmp = info[a].xpath('./div//text()')
            # 只获取第一行
            if (len(tmp)) > 0:
                result = tmp[0]
            break
    return result

def download_excel(data):
    print('all dataSize:' + str(len(data)))
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('用药助手')
    col = ['科室', '药品标签','生产企业', '通用名称', '英文名称', '商品名称', '成分', '适应症','用法用量','禁忌','毒理研究','药理作用']
    for k in range(0, 12):
        sheet.write(0, k, col[k])
    for i in range(0, len(data)):
        new_data = data[i]
        for j in range(0, 12):
            sheet.write(i + 1, j,new_data[j])
    workbook.save('/Users/heweiwen/Downloads/work/work/Python/用药助手全.xls')
    print('保存完毕')

def get_all_data():
    home_url = "https://chaoshi.detail.tmall.com/"
    # pageProps = get_pageProps(home_url)
    # firstLevelCategoryList = pageProps['firstLevelCategoryList']
    # secondLevelCategoryList = pageProps['secondLevelCategoryList']

    # login
    driver = login(home_url)
    data = []

    return data

if __name__ == '__main__':

    data = get_all_data()

    download_excel(data)