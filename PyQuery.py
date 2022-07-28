import pyppeteer
import requests
import math
import random
import json
import re, os,time
import asyncio
from pyppeteer import launch
from lxml import etree
import xlwt
from pyquery import PyQuery as pq
import ssl

width, height = 1366, 768
baseUrl = r'http://aoba.meditool.cn'
url = 'http://aoba.meditool.cn/drugs'

input = open('/Users/heweiwen/Downloads/work/work/Python/中国医学教育知识库.txt','r')
text = input.read()
list = re.split('\n', text)
location = []

# 药品库
drug_type = []
# 科室
drug_lib = []
# 药品类型列表
drug_lib_list = []
# 药品名列表
drug_name_list = []
# 药品列表
drug_list = []
# 药品详情列表
drug_detail_list = []

# 创建新page
async def create_page():
    # browser = await launch(headless=True, dumpio=True)
    browser = await launch()
    page = await browser.newPage()
    # await page.setViewport({'width': width, 'height': height})
    await page.goto(url)
    # 获取page当前显示页面的源码数据
    page_text = await page.content()
    return browser

# 运行完毕关闭browser
async def close_page(browser):
    await browser.close()


async def start(sem, url):
    # print(url)
    async with sem:  # 控制协程的并发量
        browser = create_page()
        page = await browser.newPage()
        await page.goto(url)
        print(await page.content())
        await page.close()

def parse(content):
  page_text = content.result()
  tree = etree.HTML(page_text)
  # 药品数据集合
  drug = []
  # 药品大类[例：西药]
  drug_type_span = tree.xpath('//span[@style="font-weight: bold;margin:5px 0 5px 10px;display:block;font-size:16px;"]')
  for i in range(0, len(drug_type_span)):
      # 休眠0.5s
      # time.sleep(0.5)
      type_span = drug_type_span[i].xpath('./text()')
      if len(type_span) > 0:
          drug_type.append(type_span[0])
          # 结构数据封装[药品大类]
          drug.append(type_span[0])
          #科室
          div_list = tree.xpath(
              '//div[@style="margin-left:10px;padding:15px 0 3px 0px;margin-bottom:30px;overflow: hidden"]')
          content_li = div_list[i].xpath('./li[@style="float: left;width:33%;margin-bottom:12px;"]')
          for div_li in content_li:
              drug_1 = []
              # 休眠0.5s
              time.sleep(0.5)
              content_a = div_li.xpath('./a[1]/text()')
              print('科室:'+content_a[0])
              # 科室 add
              drug_lib.append(content_a[0])
              # 结构数据封装[科室]
              drug_1.append(content_a[0])
              # 获取a标签的href属性
              content_h = div_li.xpath("./a/@href")
              # 封装url
              a_url = (baseUrl + content_h[0])
              # 获取第二次树的列表
              requests_a = requests.get(a_url)
              page_text1 = requests_a.content
              tree1 = etree.HTML(page_text1)
              # 药品标签[例：第一代头孢菌素]
              drug_tag = tree1.xpath('//span[@style="font-weight: bold;margin:5px 0 5px 10px;display:block;"]')
              # 获取标签div
              div_list1 = tree1.xpath(
                  '//div[@style="margin-left:10px;padding:15px 0 3px 0px;margin-bottom:30px;overflow: hidden"]')
              for j in range(0, len(drug_tag)):
                  drug_2 = []
                  # 休眠0.5s
                  # time.sleep(0.5)
                  tag_span = drug_tag[j].xpath('./text()')
                  if len(tag_span) > 0:
                      drug_type.append(tag_span[0])
                      # 结构数据封装[药品标签]
                      drug_2.append(tag_span[0])
                      # 获取标签div下所有li
                      content_li1 = div_list1[j].xpath('./li[@style="float: left;width:33%;margin-bottom:12px;"]')
                      for div_li1 in content_li1:
                          drug_3 = []
                          content_a1 = div_li1.xpath('./a[1]/text()')
                          # print(content_a1)
                          drug_lib_list.append(content_a1[0])
                          # 结构数据封装[药品名1]
                          drug_3.append(content_a1[0])
                          # 获取所有a标签的href属性
                          content_h1 = div_li1.xpath("./a/@href")
                          a_url1 = (baseUrl + content_h1[0])
                          # print(a_url1)
                          # 休眠0.5s
                          # time.sleep(0.5)
                          # 获取第三层树的列表
                          requests_a1 = requests.get(a_url1)
                          page_text2 = requests_a1.content
                          tree2 = etree.HTML(page_text2)
                          div_list2 = tree2.xpath('//div[@class="box_right_body clearfix"]')
                          for div_tree2 in div_list2:
                              content_a2 = div_tree2.xpath('//a[@style="margin-left:20px;color:black"]')
                              for a2 in content_a2:
                                  drug_4 = []
                                  content_a3 = a2.xpath('./text()')
                                  print(content_a3)
                                  if content_a3[0] == 'null':
                                      continue
                                  drug_name_list.append(content_a3[0])
                                  # 结构数据封装[药品名2]
                                  drug_4.append(content_a3[0])
                                  content_h2 = a2.xpath("./@href")
                                  a_url2 = (baseUrl + content_h2[0])
                                  # 获取第四层树的列表
                                  requests_a3 = requests.get(a_url2)
                                  page_text3 = requests_a3.content
                                  tree3 = etree.HTML(page_text3)
                                  # 获取药品名列表（）
                                  getDrugInfo(tree3, drug, drug_1, drug_2, drug_3, drug_4)
                                  # return location
                                  # 获取分页数据
                                  div_ul = tree3.xpath('//li')
                                  if len(div_ul) > 0:
                                      li_num = len(div_ul)
                                      last_li_num = li_num - 2
                                      last_page_num = div_ul[last_li_num].xpath('./a/text()')
                                      for num in range(2, int(last_page_num[0]) + 1):
                                          print(num)
                                          page_num_h = div_ul[2].xpath('./a/@href')
                                          if len(page_num_h) > 0:
                                              # 分页url
                                              page_num_h_str = page_num_h[0][:-1] + str(num)
                                              li_url = (baseUrl + page_num_h_str)
                                              print(li_url)
                                              requests_a4 = requests.get(li_url)
                                              page_text4 = requests_a4.content
                                              tree4 = etree.HTML(page_text4)
                                              # 获取药品名列表（）
                                              getDrugInfo(tree4, drug, drug_1, drug_2, drug_3, drug_4)
                                      # return location
  # 打印输出数据
  return location
  # 生成excel

# 单独处理每个大类Excel
def parse_for_drug(content):
  page_text = content.result()
  tree = etree.HTML(page_text)
  # 药品数据集合
  drug = []
  # 药品大类[例：西药]
  drug_type_span = tree.xpath('//span[@style="font-weight: bold;margin:5px 0 5px 10px;display:block;font-size:16px;"]')
  for i in range(0, len(drug_type_span)):
      # 休眠0.5s
      # time.sleep(0.5)
      type_span = drug_type_span[i].xpath('./text()')
      if len(type_span) > 0:
          drug_type.append(type_span[0])
          # 结构数据封装[药品大类]
          drug.append(type_span[0])
          # 科室
          div_list = tree.xpath(
              '//div[@style="margin-left:10px;padding:15px 0 3px 0px;margin-bottom:30px;overflow: hidden"]')
          content_li = div_list[i].xpath('./li[@style="float: left;width:33%;margin-bottom:12px;"]')
          for div_li in content_li:
              drug_1 = []
              # 休眠0.5s
              time.sleep(0.5)
              content_a = div_li.xpath('./a[1]/text()')
              print('科室:' + content_a[0])
              # 科室 add
              drug_lib.append(content_a[0])
              # 结构数据封装[科室]
              drug_1.append(content_a[0])
              # 获取a标签的href属性
              content_h = div_li.xpath("./a/@href")
              # 封装url
              a_url = (baseUrl + content_h[0])
              data = getDrugList(drug,drug_1,a_url)
              # 执行保存excel
              setExcel(data,content_a[0])
# 输出excel
def setExcel(data,file_name):
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('中国医学教育知识库')
    col = ['药品大类', '科室', '药品标签', '药品名称1', '药品名称2', '药品名称3', '药品英文名称', '药品成分', '适应症', '用法用量', '药物过量', '用药人群',
           'FDA妊娠药物分级', '药物相互作用', '生产企业', '剂型', '规格', '价格', '有效期', 'ATC编码', '监管分级']
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for i in range(0, len(data)):
        new_data = data[i]
        for j in range(0, len(new_data)):
            sheet.write(i + 1, j, new_data[j])
    workbook.save('/Users/heweiwen/Downloads/work/work/Python/中国医学教育知识库_'+file_name+'.xls')

#获取单科室数据
def getDrugList(drug,drug_1,url):
    # drug = ['西药']
    # drug_1 = ['抗微生物药物']
    # url = 'http://aoba.meditool.cn/typeindex/3/0'
    # 指定 特定的 url
    requests_a = requests.get(url)
    page_text1 = requests_a.content
    tree1 = etree.HTML(page_text1)
    # 药品标签[例：第一代头孢菌素]
    drug_tag = tree1.xpath('//span[@style="font-weight: bold;margin:5px 0 5px 10px;display:block;"]')
    # 获取标签div
    div_list1 = tree1.xpath(
        '//div[@style="margin-left:10px;padding:15px 0 3px 0px;margin-bottom:30px;overflow: hidden"]')
    for j in range(0, len(drug_tag)):
        drug_2 = []
        # 休眠0.5s
        # time.sleep(0.5)
        tag_span = drug_tag[j].xpath('./text()')
        if len(tag_span) > 0:
            drug_type.append(tag_span[0])
            # 结构数据封装[药品标签]
            drug_2.append(tag_span[0])
            # 获取标签div下所有li
            content_li1 = div_list1[j].xpath('./li[@style="float: left;width:33%;margin-bottom:12px;"]')
            for div_li1 in content_li1:
                drug_3 = []
                content_a1 = div_li1.xpath('./a[1]/text()')
                # print(content_a1)
                drug_lib_list.append(content_a1[0])
                # 结构数据封装[药品名1]
                drug_3.append(content_a1[0])
                # 获取所有a标签的href属性
                content_h1 = div_li1.xpath("./a/@href")
                a_url1 = (baseUrl + content_h1[0])
                # print(a_url1)
                # 休眠0.5s
                # time.sleep(0.5)
                # 获取第三层树的列表
                requests_a1 = requests.get(a_url1)
                page_text2 = requests_a1.content
                tree2 = etree.HTML(page_text2)
                div_list2 = tree2.xpath('//div[@class="box_right_body clearfix"]')
                for div_tree2 in div_list2:
                    content_a2 = div_tree2.xpath('//a[@style="margin-left:20px;color:black"]')
                    for a2 in content_a2:
                        drug_4 = []
                        content_a3 = a2.xpath('./text()')
                        print(content_a3)
                        if content_a3[0] == 'null':
                            continue
                        drug_name_list.append(content_a3[0])
                        # 结构数据封装[药品名2]
                        drug_4.append(content_a3[0])
                        content_h2 = a2.xpath("./@href")
                        a_url2 = (baseUrl + content_h2[0])
                        # 获取第四层树的列表
                        requests_a3 = requests.get(a_url2)
                        page_text3 = requests_a3.content
                        tree3 = etree.HTML(page_text3)
                        # 获取药品名列表（）
                        getDrugInfo(tree3, drug, drug_1, drug_2, drug_3, drug_4)
                        # return location
                        # 获取分页数据
                        div_ul = tree3.xpath('//li')
                        if len(div_ul) > 0:
                            li_num = len(div_ul)
                            last_li_num = li_num - 2
                            last_page_num = div_ul[last_li_num].xpath('./a/text()')
                            for num in range(2, int(last_page_num[0])+1):
                                print(num)
                                page_num_h = div_ul[2].xpath('./a/@href')
                                if len(page_num_h) > 0:
                                    # 分页url
                                    page_num_h_str = page_num_h[0][:-1] + str(num)
                                    li_url = (baseUrl + page_num_h_str)
                                    print(li_url)
                                    requests_a4 = requests.get(li_url)
                                    page_text4 = requests_a4.content
                                    tree4 = etree.HTML(page_text4)
                                    # 获取药品名列表（）
                                    getDrugInfo(tree4, drug, drug_1, drug_2, drug_3, drug_4)
                            # return location
    # 打印输出数据
    return location

# 获取药品详情
def getDrugInfo(tree3,drug,drug_1,drug_2,drug_3,drug_4):
    # 忽略tag数组
    ignore_array = ['药品图片','药品本位码','化学成分','包装','批准文号','储藏']
    # 必须tag数组
    in_array = ['药品英文名称','药品成分','适应症','用法用量','药物过量','用药人群',
           'FDA妊娠药物分级','药物相互作用','生产企业','剂型','规格','价格','有效期','ATC编码','监管分级']
    # 获取药品名列表（）
    div_list3 = tree3.xpath('//div[@class="drugdiv"]')
    for div_tree3 in div_list3:
        drug_5 = []
        content_h3 = div_tree3.xpath('./a/@href')
        a_url3 = (baseUrl + content_h3[0])
        content_a3 = div_tree3.xpath('./a[1]/text()')
        content_span = div_tree3.xpath('./span/text()')
        drug_list.append(content_a3[0])
        # 结构数据封装[药品名3]
        drug_5.append(content_a3[0])
        # 获取药品详情
        # 获取第五层树的列表
        requests_a4 = requests.get(a_url3)
        page_text4 = requests_a4.content
        tree4 = etree.HTML(page_text4)
        # 获取药品属性
        getDrugDetail(tree4,drug_5)
        # 添加到全局Data
        location.append(drug + drug_1 + drug_2 + drug_3 + drug_4 + drug_5)

# 获取药品属性
def getDrugDetail(tree4,drug_5):
    result = tree4.xpath('//div[@class="drugdiv"]/span/text()')
    title = tree4.xpath('//div[@style="margin-bottom:15px;color:#427dc9"]/a/text()')
    # 获取动态 说明书 keyName
    sms_name = tree4.xpath('//span[@style="color: #a0a0a0"]/text()')
    # name = result[0]
    if len(result) > 1:
        e_name = result[1]
        drug_5.append(e_name)
    else:
        drug_5.append('e_name')
    # sms_name_en = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),'+sms_name+')]/../span[2]/text()')
    ypcf = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"药品成分")]/../span[2]/text()')
    syz = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"适应症")]/../span[2]/text()')
    yfyl = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"用法用量")]/../span[2]/text()')
    ywgl = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"药物过量")]/../span[2]/text()')
    yyrq = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"用药人群")]/../span[2]/text()')
    fda = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"FDA妊娠药物分级")]/../span[2]/text()')
    ywxhzy = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"药物相互作用")]/../span[2]/text()')
    compay = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"生产企业")]/../span[2]/text()')
    jx = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"剂型")]/../span[2]/text()')
    gg = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"规格")]/../span[2]/text()')
    jg = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"价格")]/../span[2]/text()')
    yxq = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"有效期")]/../span[2]/text()')
    atc = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"ATC编码")]/../span[2]/text()')
    jgfj = tree4.xpath('//div[@class="drugdiv"]/span[contains(text(),"监管分级")]/../span[2]/text()')
    # drug_5.append(name)
    drug_5.append(ypcf)
    drug_5.append(syz)
    drug_5.append(yfyl)
    drug_5.append(ywgl)
    drug_5.append(yyrq)
    drug_5.append(fda)
    drug_5.append(ywxhzy)
    drug_5.append(compay)
    drug_5.append(jx)
    drug_5.append(gg)
    drug_5.append(jg)
    drug_5.append(yxq)
    drug_5.append(atc)
    drug_5.append(jgfj)
    # 添加到全局Data
    return drug_5


async def getHref(Url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(Url)
    page_text1 = page.content()
    return page_text1



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

def getUrlInfo(content):
    # 指定 特定的 url
    page_text = content.result()
    tree = etree.HTML(page_text)
    drug_tag = tree.xpath('//div[@class="item__3ue7"]')
    info = tree.xpath('//div[@class="content__1KNL"]')
    for i in range(0, len(drug_tag)):
        type = drug_tag[i].xpath('./div[@class="cnName__3Kpx"]/text()')
        if type[1] == '用法用量':
            print(type)
            info_str = info[i].xpath('./p/text()')
            print(info_str)

def download_excel(content):
    # parse_for_drug(content)
    drug = ['中药']
    drug_1 = ['儿科用药']
    url = 'http://aoba.meditool.cn/childtype'
    # data = parse(content)
    data = getDrugList(drug,drug_1,url)
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('中国医学教育知识库')
    col = ['药品大类','科室','药品标签','药品名称1','药品名称2','药品名称3','药品英文名称','药品成分','适应症','用法用量','药物过量','用药人群',
           'FDA妊娠药物分级','药物相互作用','生产企业','剂型','规格','价格','有效期','ATC编码','监管分级']
    for i in range(0, len(col)):
        sheet.write(0, i, col[i])
    for i in range(0, len(data)):
        new_data = data[i]
        for j in range(0, len(new_data)):
            sheet.write(i + 1, j,new_data[j])
    workbook.save('/Users/heweiwen/Downloads/work/work/Python/中国医学教育知识库/中国医学教育知识库_'+drug_1[0]+'.xls')
    print('保存完毕')

def main():
    # url = 'https://drugs.dxy.cn/drug/5qQdaJPF1D8wKhn7kP12DA=='
    url = 'http://aoba.meditool.cn/drugs'
    task = get_html(url)
    return task


c = main()
task = asyncio.ensure_future(c)
task.add_done_callback(download_excel)
loop = asyncio.get_event_loop()
loop.run_until_complete(c)