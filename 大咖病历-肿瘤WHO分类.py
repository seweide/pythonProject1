import pyppeteer
import requests
import urllib.request
from bs4 import BeautifulSoup
import re, os,time
import asyncio
from lxml import etree
import xlsxwriter

location = []

baseUrl = 'http://dia.dakapath.com/'

async def get_html(url):
    browser = await pyppeteer.launch(headless=True, args=['--no-sandbox'])
    page = await  browser.newPage()
    res = await page.goto(url, options={'timeout': 3000})
    data = await page.content()
    title = await page.title()
    resp_cookies = await page.cookies()  # cookie
    resp_headers = res.headers  # 响应头
    resp_status = res.status  # 响应状态
    return data

#请求Url，返回html
def url_open(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def iterate_files(content):
    page_text = content.result()
    tree = etree.HTML(page_text)
    # 药品数据集合

    drug_type_span = tree.xpath('//div[@class="catResultList2"]')
    for i in range(0, len(drug_type_span)):
        drug = []
        # 获取H4
        drug_h4 = drug_type_span[i].xpath('./h4/text()')
        print('drug_h4:'+drug_h4[0])
        drug.append(drug_h4[0])
        drug_p = drug_type_span[i].xpath('./p[@class="sublinks"]')
        for p in drug_p:
            a_text = p.xpath('./a/text()')
            print('drug_p:'+a_text[0])
            if len(a_text) > 0:
                for j in range(0, len(a_text)):
                    drug_1 = []
                    drug_1.append(a_text[j])
                    a_href = p.xpath("./a/@href")
                    print('a_href:' + a_href[j])
                    # 封装url
                    a_url = (baseUrl + a_href[j])
                    # 获取第二次树的列表
                    # requests_a = requests.get(a_url)
                    # page_text1 = requests_a.content
                    # tree1 = etree.HTML(page_text1)
                    # 药品标签[例：第一代头孢菌素]
                    # drug_sm_h2 = tree1.xpath('//div[@class="col-sm-9"]/h2/text()')

                    # 拿到a标签的url，获取HTML
                    try:
                        districtHtml = url_open(a_url)
                    except Exception:
                        print("出异常啦，努力重试中")
                        # 速度过快可能会被封掉，休息5S再重试
                        time.sleep(5)
                        districtHtml = url_open(a_url)
                    districtSoup = BeautifulSoup(districtHtml)
                    # drug_sm_h2 = districtSoup.xpath('//div[@class="col-sm-9"]/h2/text()')
                    drug_sm_h2 = districtSoup.find("div", class_="col-sm-9")
                    drug_sm_h2_arr = drug_sm_h2.contents
                    if len(drug_sm_h2_arr) > 0:
                        drug_2 = []
                        drug_1.append(drug_sm_h2_arr[0])
                        for j in range(1, len(drug_sm_h2_arr)):
                            drug_span = ''
                            tag_span = drug_sm_h2_arr[j]
                            try:
                                if tag_span.contents:
                                    drug_span_1 = tag_span.contents
                                    if len(drug_span_1) > 1:
                                        if isinstance(drug_span_1[0], str):
                                            drug_span = drug_span + drug_span_1[0]
                                        tag_type = isinstance(drug_span_1[1], str)
                                        if tag_type:
                                            drug_2.append(drug_span)
                                            continue
                                        else:
                                            for k in range(1, len(drug_span_1)):
                                                tag_type = isinstance(drug_span_1[k], str)
                                                if tag_type:
                                                    drug_span_2 = drug_span_1[k]
                                                    drug_span = drug_span + drug_span_2
                                                else:
                                                    if drug_span_1[k].contents:
                                                        drug_span_2 = drug_span_1[k].contents
                                                        if isinstance(drug_span_2[0], str):
                                                            drug_span_3 = drug_span_2[0]
                                                            drug_span = drug_span + drug_span_3
                                                        else:
                                                            if drug_span_2[0].contents:
                                                                drug_span_3 = drug_span_2[0].contents
                                                                if isinstance(drug_span_3[0], str):
                                                                    drug_span_4 = drug_span_3[0]
                                                                    drug_span = drug_span + drug_span_4
                                                                else:
                                                                    if drug_span_3[0].contents:
                                                                        drug_span_4 = drug_span_3[0].contents
                                                                        if isinstance(drug_span_4[0], str):
                                                                            drug_span_5 = drug_span_4[0]
                                                                            drug_span = drug_span + drug_span_5
                                                                        else:
                                                                            drug_span_5 = drug_span_4[0].contents
                                                                            if isinstance(drug_span_5[0], str):
                                                                                drug_span_6 = drug_span_5[0]
                                                                                drug_span = drug_span + drug_span_6
                                                                            else:
                                                                                drug_span_6 = drug_span_5[0].contents
                                                                                drug_span = drug_span + drug_span_6
                                    else:
                                        drug_span = drug_span + drug_span_1[0]

                            except AttributeError:
                                print('Error: worksheetwrite_row失败')
                                if drug_span != '' or len(drug_span) > 0:
                                    drug_2.append(drug_span)
                                continue
                            drug_2.append(drug_span)
                    # 封装 行
                    location.append(drug + drug_1 + drug_2)

    return location



def data_to_excel(content):
    data = iterate_files(content)
    # 新建excel表
    workbook = xlsxwriter.Workbook('/Users/heweiwen/Downloads/work/work/Python/大咖病历-肿瘤WHO分类.xls')
    # 新建sheet（sheet的名称为"sheet1"）
    worksheet = workbook.add_worksheet('大咖病历-肿瘤WHO分类')
    # 设置表头
    headings = ['通用名称','商品名称','英文名称','适应症','不良反应','注意事项','禁忌','药物过量','药理毒理','执行标准','企业名称']
    worksheet.write_row('A1', headings)
    i = 2
    for row in data:
        i = i + 1
        try:
            worksheet.write_row('A' + str(i), row)
        except KeyError:
            print('Error: worksheetwrite_row失败')
            continue

    # 将excel文件保存关闭，
    workbook.close()
    print('保存完毕')


def main():
    print('html-解析-开始')
    url = 'http://dia.dakapath.com/home/article/tumourwho.html'
    task = get_html(url)
    return task



c = main()
task = asyncio.ensure_future(c)
task.add_done_callback(data_to_excel)
loop = asyncio.get_event_loop()
loop.run_until_complete(c)