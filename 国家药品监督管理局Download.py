import pyppeteer
import requests
import asyncio
import random
import json
import re, os,time
import asyncio
from pyppeteer import launch
from lxml import etree
import xlwt
from pyquery import PyQuery as pq
import ssl
import logging
import sys
import urllib

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

#全局word集合
download = []
down_BaseUrl = 'http:'
down_pageUrl = 'http://202.96.26.102/index/instruction?&page='

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO,
    stream=sys.stdout)

#下载国家药品监督管理局说明书
def download_word(content):
    page_text = content.result()
    tree = etree.HTML(page_text)
    getTableInfo(tree)
    #总页数（1654）
    page_num = int(1654 / 10)
    for num in range(2, page_num):
        # 休眠0.5s
        time.sleep(0.5)
        print(num)
        # 分页url
        url = (down_pageUrl + str(num))
        print(url)
        requests_page = requests.get(url)
        text = requests_page.content
        tree1 = etree.HTML(text)
        # 获取表格内容
        getTableInfo(tree1)

    # 返回list
    return download


# 获取表格内容
def getTableInfo(tree):
    drug_table = tree.xpath('//tbody/tr')
    for table in drug_table:
        word_download_url = []
        drug_td = table.xpath('./td')
        for i in range(0,len(drug_td)):
            value = ''
            url = ''
            urlname = ''
            if i == 3:
                value = drug_td[i].xpath('./a/@href')
                if len(value) > 0:
                    # 截取文件名字
                    value_s = value[0].split('/')
                    urlname = value_s[-1]
                    url = down_BaseUrl + value[0]
            else:
                value = drug_td[i].xpath('./text()')

            if len(value) > 0:
                if url is not '':
                    word_download_url.append(url)
                else:
                    word_download_url.append(value[0])
            else:
                word_download_url.append('')
        download.append(word_download_url)
        # 触发下载
        if url is not '' and urlname is not '':
            urldownload(url,urlname)
            # urlretrieve(url,urlname)


def urldownload(url,filename=None):
    """
    下载文件到指定目录
    :param url: 文件下载的url
    :param filename: 要存放的目录及文件名，例如：./test.xls
    :return:
    """
    file_path = os.path.join(os.getcwd(), '国家药品监督管理局说明书/')
    file_dir = file_path[:-1]
    if not os.path.exists(file_dir):
        logging.info("Mkdir '国家药品监督管理局说明书/'.")
        os.mkdir(file_dir)

    file_path = file_dir + '/' + filename

    down_res = requests.get(url)
    with open(file_path,'wb') as file_path:
        file_path.write(down_res.content)

def urlretrieve(url,filename=None):

    file_path = os.path.join(os.getcwd(), '国家药品监督管理局说明书/')
    if not os.path.isfile(file_path):
        logging.info("File doesn't exist.")
        # replace with url you need

        # if dir 'dir_name/' doesn't exist /H20130022.doc
        file_dir = file_path[:-1]
        if not os.path.exists(file_dir):
            logging.info("Mkdir '国家药品监督管理局说明书/'.")
            os.mkdir(file_dir)

        file_path = file_dir + '/' + filename

        def down(_save_path, _url):
            try:
                urllib.urlretrieve(_url, _save_path)
            except:
                print('\nError when retrieving the URL:', _save_path)

        logging.info("Downloading file.")
        down(file_path, url)
    else:
        logging.info("File exists.")

def download_excel(content):
    # data = parse(content)
    data = download_word(content)
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('国家药品监督管理局说明书')
    col = ['批准文号/注册证号','药品名称','企业名称','说明书附件']
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for i in range(0, len(data)):
        new_data = data[i]
        for j in range(0, len(new_data)):
            sheet.write(i + 1, j,new_data[j])
    workbook.save('/Users/heweiwen/Downloads/work/work/Python/国家药品监督管理局说明书.xls')
    print('保存完毕')

def main():
    url = 'http://202.96.26.102/index/instruction?&page=1'
    task = get_html(url)
    return task


c = main()
task = asyncio.ensure_future(c)
task.add_done_callback(download_excel)
loop = asyncio.get_event_loop()
loop.run_until_complete(c)