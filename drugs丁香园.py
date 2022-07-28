from selenium import webdriver
import requests
from lxml import etree
import time
from bs4 import BeautifulSoup
import json as js

if __name__ == '__main__':
    chromedriver = "/Users/heweiwen/Downloads/work/Solf/chrome-mac/chromedriver"
    driver = webdriver.Chrome(executable_path=chromedriver)
    home_url = "https://drugs.dxy.cn"
    driver.get(home_url)  # 打开网址
    driver.get(home_url)
    drugs_1 = etree.HTML(driver.page_source)
    drugs_1_list = drugs_1.xpath('//div[@class="category-tab__37us"]/span/text()')
    drugs_1_tab = drugs_1.xpath('//div[@class="ant-tabs-tab"]')

    html = driver.page_source
    # BeautifulSoup转换页面源码
    bs = BeautifulSoup(html, 'lxml')
    # 获取Script标签下的完整json数据，并通过json加载成字典格式
    contents = bs.find("script", {"id": "__NEXT_DATA__"}).contents
    # json 父子级别
    js_test = {}
    pageProps = {}
    # 父级
    firstLevelCategoryList = []
    # 子级
    secondLevelCategoryList = []
    # firstjson
    for i in range(0, len(contents)):
        print(contents[i])
        js_test = js.loads(contents[i])
        pageProps = js_test['props']['pageProps']
        # pageProps = js.dumps(contents[i]).find('props')
    firstLevelCategoryList = pageProps['firstLevelCategoryList']
    secondLevelCategoryList = pageProps['secondLevelCategoryList']

    for f in firstLevelCategoryList:
        id = f['id']
        name = f['name']
        # 获取所有子集
        secondsList = []
        for s in secondLevelCategoryList:
            if s['supId'] == id:
                seconds = {}
                seconds['id'] = s['id']
                seconds['name'] = s['name']
                seconds['supId'] = s['supId']
                seconds['recommendDrugs'] = s['recommendDrugs']
                secondsList.append(seconds)


    for i in range(0, len(drugs_1_tab)):
        driver.find_element_by_xpath('//div[@style="margin-bottom:0"]').click()
    drugs_1_tabpanel = drugs_1.xpath('//div[@role="tabpanel"]')

    for div in drugs_1_tab:
        # driver.find_element_by_xpath('//div[@class="ant-tabs-tab"]').click()
        # bottom = div.xpath('./div[@class="ant-tabs-tab-btn"]/@id')
        id = div.xpath('./div[@class="ant-tabs-tab-btn"]/@id')
        print(id)
    for div in drugs_1_tabpanel:
        tabpanel_names = div.xpath('./ul/li[@class="category-item__ZnzJ"]')
        for div_1 in tabpanel_names:
            nams = div_1.xpath('./h3/a/text()')
            print(nams)