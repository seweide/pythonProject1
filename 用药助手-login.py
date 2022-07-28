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
    ypbq = sel.xpath('//div[@class="category-header__3owX"]/h2/text()')[0]
    total = sel.xpath('//span[@class="category-header-count__27vs"]/text()')[0]
    print('药品标签:'+ ypbq)
    print('总条数:'+total)
    total_page = math.ceil(int(total)/10)
    print('总页数：'+str(total_page))

    #分页查询
    for page in range(0,int(total_page)):
        pageurl = category + '?page=' + str(page+1)
        url = home_url + pageurl
        print('url:' + url)
        driver.get(url)
        time.sleep(0.2)
        sel = etree.HTML(driver.page_source)
        result1 = sel.xpath('//h3[@class="drugs-item-name__3yfj"]/a/@href')
        result2 = sel.xpath('//h3[@class="drugs-item-name__3yfj"]/a/text()')

        for i in range(0, len(result1)):
            list = []
            detail_url = 'https://drugs.dxy.cn' + result1[i]
            #print('detail_url:'+detail_url)
            driver.get(detail_url)
            time.sleep(0.5)
            detail_sel = etree.HTML(driver.page_source)
            t_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"通用名称")]/text()')
            y_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"英文名称")]/text()')
            s_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"商品名称")]/text()')

            list.append(keshi) #科室
            list.append(ypbq) #药品标签
            # 生产企业
            if result1[i] == '/drug/CLa3tUplspls5S3pIMfplsplsPcEPpCw==': #特殊处理
                company = '天津市天骄制药有限公司'
            else:
                company = result2[i*3+2]
            list.append(company) #生产企业
            list.append(get_name(t_name)) #通用名称
            list.append(get_name(y_name)) #英文名称
            list.append(get_name(s_name)) #商品名称
            drug_tag = detail_sel.xpath('//div[@class="item__3ue7"]')
            info = detail_sel.xpath('//div[@class="content__1KNL"]')
            list.append(get_cf(drug_tag, info, '成份'))
            list.append(get_context(drug_tag, info, '适应症'))
            list.append(get_context(drug_tag, info, '用法用量'))
            list.append(get_context(drug_tag, info, '禁忌'))
            list.append(get_context(drug_tag, info, '毒理研究'))
            list.append(get_context(drug_tag, info, '药理作用'))

            data.append(list)
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
    cookie1 = {"name": "CLASS_CASTGC",
               "value": "59abc8e78c52098313bc349d45c5c9050adb83c281a3165f79016877480adcb45baf4bfc1e3b16b222064a51b3bad756966757757d19b9aef265690068c98212b0179181736a3075aaf7890a0ab6a9d8a28c3a5bb0d1316f2b2c1ad8fad515b8fbfb98731fa4831bc64ee33b31a015cff1aa3f97063832a3f43d53317f0f36a89ab0e72e7a42693a3e9e984f605e425d66e363aa77008f59f42de37c9552e33e2543a63f122922a47521d42cadbfa39e71d42cd199699c08d2d99c941ac95607038212cadf7d910654f7576ab863a24042ddadde88d548e65a83fcbb5fe2f09be0ad84a30316859fc303b3201385af77d83af1dfed328fe83f193f3594e1538e"}
    cookie2 = {"name": "dxy_da_cookie-id", "value": "2271a6bc57ad28abdc5e0d50bd03aa961619056600265"}
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

# 获取适应症，用法用量，禁忌，毒理研究，药理作用的通用方法
def get_context(drug_tag,info,name):
    result = ""
    for i in range(0, len(drug_tag)):
        type = drug_tag[i].xpath('./div[@class="cnName__3Kpx"]/text()')
        if len(type) == 3:
            if type[1] == name:
                tmp = info[i].xpath('./div//text()')
                if (len(tmp)) > 0:
                    for b in range(0, len(tmp)):
                        result = result + tmp[b].strip()
                break
        else:
            if len(type) == 1:
                tmpType = type[0].replace('【','】')
                if tmpType == name:
                    tmp = info[i].xpath('./div//text()')
                    if (len(tmp)) > 0:
                        for b in range(0, len(tmp)):
                            result = result + tmp[b].strip()
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
    home_url = "https://drugs.dxy.cn"
    pageProps = get_pageProps(home_url)
    firstLevelCategoryList = pageProps['firstLevelCategoryList']
    secondLevelCategoryList = pageProps['secondLevelCategoryList']

    driver = login(home_url) #login
    data = []

    for f in firstLevelCategoryList:
        id = f['id']
        keshi = f['name']
        print('keshi:' + keshi)
        #if keshi == '消化系统及代谢药' or keshi == '血液和造血系统药物' or keshi == '心血管系统药物' or keshi == '皮肤病用药':
            #continue
        for s in secondLevelCategoryList:
            if s['supId'] == id:
                if s['id'] == '4NG2M2B4kg4ZpXkT9nX94Q==' or s['id'] == '0T2Hyma47PcxkUwXXcbBdg==':
                    print("刺激食欲药,外科敷料 网页无法打开")
                else:
                    category_url = '/category/' + s['id']
                    print(category_url)
                    data = get_data(home_url, driver, data, category_url, keshi)
                    print('dataSize:' + str(len(data)))

    return data

if __name__ == '__main__':

    data = get_all_data()

    download_excel(data)