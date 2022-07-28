#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import xlwt

def download_excel():
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('test')
    col = ['药理分类1', '药理分类2', '通用名称', '英文名称', '商品名称', '成分', '适应症','生产企业']
    for i in range(0, 8):
        sheet.write(0, i, col[i])

    workbook.save('D:\Python\ExcelTest.xls')
    print('保存完毕')

if __name__ == '__main__':
    download_excel()
