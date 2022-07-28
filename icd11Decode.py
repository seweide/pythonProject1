import pyppeteer
import requests
import urllib.request
import json as js
import xlwt
from bs4 import BeautifulSoup
import re, os,time
import asyncio
from lxml import etree
import xlsxwriter
import zipfile
from selenium import webdriver
import requests
from lxml import etree
import time
from bs4 import BeautifulSoup
import json as js

url_detail = 'https://icd11.pumch.cn/api/services/app/MMS/GetMMSDetailFromId'
title_arr = []
definition_arr = []

async def get_html(url):
    browser = await pyppeteer.launch(headless=True, args=['--no-sandbox'])
    page = await  browser.newPage()
    res = await page.goto(url, options={'timeout': 3000})
    data = await page.content()
    title = await page.title()
    resp_cookies = await page.cookies()  # cookie
    resp_headers = res.headers  # 响应头
    resp_status = res.status  # 响应状态
    # print(data)
    # print(title)
    # print(resp_headers)
    # print(resp_status)
    return data

def request_url_get(url, false=None):
    # url = 'https://icd11.pumch.cn/api/services/app/MMS/GetMMSNodes?refId=&classKind=&isAdoptedChild=false'
    # url_node = 'https://icd11.pumch.cn/api/services/app/MMS/GetMMSNodes?refId='
    # url_node_end = '&classKind='
    # url_node_end2 = '&isAdoptedChild=false'
    # url_node = url_node + refId + url_node_end + classKind + url_node_end2
    url_node2 = 'https://icd11.pumch.cn/api/services/app/MMS/GetMMSNodes'
    # ignore_arr = [
    #     '1435254666'
    #     ,'1296093776'
    #     ,'1630407678'
    #     ,'1766440644'
    #     ,'1954798891'
    #     ,'334423054'
    #     ,'21500692'
    #     ,'274880002'
    #     ,'868865918'
    #     ,'1218729044'
    #     ,'426429380'
    #     ,'197934298'
    #     ,'1256772020'
    #     ,'1639304259'
    #     ,'1473673350'
    #     ,'30659757'
    #     ,'577470983'
    #     ,'714000734'
    #     ,'1306203631'
    #     ,'223744320'
    #     ,'1843895818'
    #     ,'435227771'
    #     ,'850137482'
    #     ,'1249056269'
    #     ,'1596590595'
    #     ,'718687701'
    #     ,'231358748'
    #     ,'979408586'
    #               ]
    ignore_arr = ['21500692',
                    '30659757',
                    '197934298',
                    '231358748',
                    '274880002',
                    '334423054',
                    '426429380',
                    '718687701',
                    '850137482',
                    '868865918',
                    '979408586',
                    '1218729044',
                    '1249056269',
                    '1256772020',
                    '1296093776',
                    '1435254666',
                    '1473673350',
                    '1596590595',
                    '1630407678',
                    '1639304259',
                    '1766440644',
                    '1954798891']
    re = requests.get(url)
    text_str = re.text
    js_test = js.loads(text_str)
    result = js_test['result']
    for a in result:
        return_arr = []
        name = a['refId'] +'_'+ a['code']
        print('name:' +name)
        if a['refId'] in ignore_arr:
            continue
        package_code(a,return_arr)
        hasChildren = a['hasChildren']
        x = type(hasChildren)
        if a['refId'] or ('1' is x):
            #获取结果
            result = get_page_info(a,url_node2)
            for a in result:
                package_code(a, return_arr)
                hasChildren = a['hasChildren']
                x = type(hasChildren)
                if a['refId'] or ('1' is x):
                    # 获取结果
                    result = get_page_info(a, url_node2)
                    for a in result:
                        package_code(a, return_arr)
                        hasChildren = a['hasChildren']
                        x = type(hasChildren)
                        if a['refId'] or ('1' is x):
                            # 获取结果
                            result = get_page_info(a, url_node2)
                            for a in result:
                                package_code(a, return_arr)
                                hasChildren = a['hasChildren']
                                x = type(hasChildren)
                                if a['refId'] or ('1' is x):
                                    # 获取结果
                                    result = get_page_info(a, url_node2)
                                    for a in result:
                                        package_code(a, return_arr)
        download_excel(return_arr,name)
    # return return_arr

#封装title
def package_title(Translations,ret_a,return_arr):
    for list in Translations:
        if list['title']:
            print('title:' + list['title'])
            ret_a.append(list['title'])
        else:
            ret_a.append('null')
        if list['definition']:
            ret_a.append(list['definition'])
        else:
            ret_a.append('null')
        return_arr.append(ret_a)

#封装linearizationTranslationApis
def package_Apis(TranslationApis,ret_a):
    for list in TranslationApis:
        # if list['title']:
        #     print('title:' + list['title'])
        #     title_arr.append(list['title'])
        #     ret_a.append(list['title'])
        if list['definition']:
            definition_arr.append(list['definition'])
            ret_a.append(list['definition'])
        else:
            ret_a.append('null')

def package_code(a,return_arr):
    ret_a = []
    if a['refId']:
        # print('refId:' + a['refId'])
        ret_a.append(a['refId'])
    else:
        ret_a.append('null')
    if a['parentRefId']:
        # print('parentRefId:' + a['parentRefId'])
        ret_a.append(a['parentRefId'])
    else:
        ret_a.append('null')
    # print('hasChildren:' + a['hasChildren'])
    if a['codeRange']:
        # print('codeRange:' + a['codeRange'])
        ret_a.append(a['codeRange'])
    else:
        ret_a.append('codeRange_null')
    if a['code']:
        # print('code:' + a['code'])
        ret_a.append(a['code'])
    else:
        ret_a.append('code_null')

    #获取描述
    if a['linearizationTranslations']:
        package_title(a['linearizationTranslations'], ret_a, return_arr)

    #获取详情（英文名）
    return_detail = get_page_detail(a['refId'],url_detail)
    if return_detail['linearizationTranslationApis']:
        package_Apis(return_detail['linearizationTranslationApis'], ret_a)


def get_page_info(a,url_node2,false=None):
    # 休眠0.5s
    time.sleep(1)
    # print('refId:' + a['refId'])
    refId = a['refId']
    classKind = 'category'
    if a['classKind']:
        # print('classKind:' + a['classKind'])
        classKind = a['classKind']
    # 将携带的参数传给params
    data = {'refId': refId, 'classKind': classKind, 'isAdoptedChild': false}
    r = requests.get(url_node2, params=data)
    text_str = r.text
    js_test = js.loads(text_str)
    result = js_test['result']
    return result

def get_page_detail(refId,url_detail):
    # 休眠0.5s
    time.sleep(1)
    # 将携带的参数传给params
    data = {'refId': refId}
    r = requests.get(url_detail, params=data)
    text_str = r.text
    js_test = js.loads(text_str)
    result = js_test['result']
    return result

def download_excel(data,name):
    # url = 'https://icd11.pumch.cn/api/services/app/MMS/GetMMSNodes?refId=&classKind=&isAdoptedChild=false'
    # data = request_url_get(url)
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('ICD-11-死因和疾病统计')
    col = ['refId','parentRefId','编码CodeRange','编码Code','疾病名称','描述','英文描述']
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for i in range(0, len(data)):
        new_data = data[i]
        for j in range(0, len(new_data)):
            try:
                sheet.write(i + 1, j,new_data[j])
            except KeyError:
                print('Error: worksheetwrite_row失败')
                continue

    workbook.save('/Users/heweiwen/Downloads/work/work/Python/ICD-11-死因和疾病统计_解析Excel_'+name+'.xls')
    print('保存完毕')

if __name__ == '__main__':
    # chromedriver = "/Users/heweiwen/Downloads/work/Solf/chrome-mac/chromedriver"
    # driver = webdriver.Chrome(executable_path=chromedriver)
    # home_url = "https://drugs.dxy.cn"
    # driver.get(home_url)  # 打开网址
    # driver.get(home_url)
    # drugs_1 = etree.HTML(driver.page_source)
    # drugs_1_list = drugs_1.xpath('//div[@class="category-tab__37us"]/span/text()')
    # drugs_1_tab = drugs_1.xpath('//div[@class="ant-tabs-tab"]')
    #
    # html = driver.page_source

    url = 'https://icd11.pumch.cn/api/services/app/MMS/GetMMSNodes?refId=&classKind=&isAdoptedChild=false'
    data = request_url_get(url)