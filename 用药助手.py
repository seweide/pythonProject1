#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
import xlwt

def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'
    }
    home_url = 'https://drugs.dxy.cn'
    category = '/category/W0wXLapCLBwplsplsZcunULmepepmmXA=='
    url = home_url + category
    res = requests.get(url,headers=headers)
    sel = etree.HTML(res.content)
    total = sel.xpath('//span[@class="category-header-count__27vs"]/text()')[0]
    print('总条数:'+total)

    ylfl1 = '抗肿瘤和免疫调节'
    ylfl2 = sel.xpath('//div[@class="category-header__3owX"]/h2/text()')[0]

    data = []
    total_page = int(total)/10
    print('总页数：'+str(total_page))

    for page in range(0,5):
        category = '/category/W0wXLapCLBwplsplsZcunULmepepmmXA==' + '?page=' + str(page+1)
        url = home_url + category
        print('url:' + url)
        res = requests.get(url, headers=headers).content
        sel = etree.HTML(res)
        result1 = sel.xpath('//h3[@class="drugs-item-name__3yfj"]/a/@href')
        result2 = sel.xpath('//h3[@class="drugs-item-name__3yfj"]/a/text()')
        result4 = sel.xpath('//p[@class="drugs-item-content__39X7"]/span/text()')
        #print(result1)
        #print(result4)

        for i in range(0, len(result1)):
            list = []
            detail_url = 'https://drugs.dxy.cn' + result1[i]
            print('detail_url:'+detail_url)
            detail_res = requests.get(detail_url, headers=headers).content
            detail_sel = etree.HTML(detail_res)
            t_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"通用名称")]/text()')
            y_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"英文名称")]/text()')
            s_name = detail_sel.xpath('//div[@class="drug-names__8L2q"]/p[contains(text(),"商品名称")]/text()')
            list.append(ylfl1)
            list.append(ylfl2)
            list.append(t_name[1])
            list.append(y_name[1])
            list.append(s_name[1])
            list.append(result4[i*2])
            list.append(result4[i*2+1])
            list.append(result2[i*3+2])
            data.append(list)
    #print(data)
    return data

def download_excel():
    data = get_data()
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('用药助手')
    col = ['药理分类1', '药理分类2', '通用名称', '英文名称', '商品名称', '成分', '适应症','生产企业']
    for i in range(0, 8):
        sheet.write(0, i, col[i])
    for i in range(0, len(data)):
        new_data = data[i]
        for j in range(0, 8):
            sheet.write(i + 1, j,new_data[j])
    workbook.save('D:\Python\用药助手.xls')
    print('保存完毕')

if __name__ == '__main__':
    download_excel()