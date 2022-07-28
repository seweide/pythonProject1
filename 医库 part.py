#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
import xlwt



def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:50.0) Gecko/20100101 Firefox/50.0'
    }
    url1 = 'http://aoba.meditool.cn/drugs'

    sel = etree.HTML(requests.get(url1, headers=headers).content)
    href_list1 = sel.xpath('//li[@style="float: left;width:33%;margin-bottom:12px;"]/a/@href')

    for i in range(0, len(href_list1)):
        data = []
        url2 = 'http://aoba.meditool.cn/' + href_list1[i]
        print('url2:'+url2)

        # 药品大类
        if href_list1[i] == ('/typeindex/2/-4') or href_list1[i] == ('/childtype/'):
            ypdl = '用药人群'
        if href_list1[i].startswith('/chinatype/'):
            ypdl = '中药'
        else:
            ypdl = '西药'
        print(ypdl)
        sel = etree.HTML(requests.get(url2, headers=headers).content)
        #href_list2 = sel.xpath('//li[@style="float: left;width:33%;margin-bottom:12px;"]/a/@href')

        # 药品标签list
        ypbq_list = sel.xpath('//span[@style="font-weight: bold;margin:5px 0 5px 10px;display:block;"]//text()')
        # 与药品标签同级
        div_list1 = sel.xpath('//div[@style="margin-left:10px;padding:15px 0 3px 0px;margin-bottom:30px;overflow: hidden"]')

        for j in range(0,len(div_list1)):
            li_list = div_list1[j].xpath('./li[@style="float: left;width:33%;margin-bottom:12px;"]')

            ypbq = ypbq_list[j]
            print(ypbq)

            for h in range(0,len(li_list)):
                # content_a1 = li.xpath('./a[1]/text()')
                href_list2 = li_list[h].xpath("./a/@href")
                print(href_list2)

                url3 = 'http://aoba.meditool.cn/' + href_list2[0]
                print('url3:' + url3)

                sel = etree.HTML(requests.get(url3, headers=headers).content)
                href_list3 = sel.xpath('//div[@class="box_right_body clearfix"]/a/@href')
                # print(href_list3)

                for k in range(0, len(href_list3)):
                    url4 = 'http://aoba.meditool.cn/' + href_list3[k]
                    print('url4:' + url4)
                    sel = etree.HTML(requests.get(url4, headers=headers).content)

                    totalpage = '1'
                    pageAll = sel.xpath('//ul[@class="pagination"]/li/a/@href')
                    #print(pageAll)
                    # 判断是否有分页
                    if len(pageAll) > 0:
                        lastpage = pageAll[len(pageAll) - 2]
                        totalpage = lastpage[-1]

                    print('totalpage：' + totalpage)

                    for page in range(0, int(totalpage)):
                        if page > 0:
                            url4 = 'http://aoba.meditool.cn/' + href_list3[k] + '?page=' + str(page + 1)
                            print('url4:' + url4)
                            sel = etree.HTML(requests.get(url4, headers=headers).content)

                        #print('page---->'+ str(page))
                        href_list4 = sel.xpath('//div[@class="drugdiv"]/a/@href')
                        #print(href_list4)

                        for l in range(0, len(href_list4)):
                            list = []
                            url5 = 'http://aoba.meditool.cn/' + href_list4[l]
                            # print('url5:'+url5)
                            sel = etree.HTML(requests.get(url5, headers=headers).content)
                            result = sel.xpath('//div[@class="drugdiv"]/span/text()')
                            title = sel.xpath('//div[@style="margin-bottom:15px;color:#427dc9"]/a/text()')

                            # 药品大类
                            list.append(ypdl)
                            # 科室
                            keshi = title[2]
                            list.append(keshi)
                            list.append(ypbq)
                            # 药品名称1
                            list.append(title[3])
                            # 药品名称2
                            list.append(title[4])
                            # 药品名称3
                            name = ''
                            e_name = ''
                            if len(result) > 0:
                                name = result[0]
                            if len(result) > 1:
                                e_name = result[1]
                            list.append(name)
                            list.append(e_name)

                            ypcf = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"药品成分")]/../span[2]/text()')
                            syz = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"适应症")]/../span[2]/text()')
                            yfyl = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"用法用量")]/../span[2]/text()')
                            ywgl = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"药物过量")]/../span[2]/text()')
                            yyrq = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"用药人群")]/../span[2]/text()')
                            fda = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"FDA妊娠药物分级")]/../span[2]/text()')
                            ywxhzy = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"药物相互作用")]/../span[2]/text()')
                            compay = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"生产企业")]/../span[2]/text()')
                            jx = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"剂型")]/../span[2]/text()')
                            gg = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"规格")]/../span[2]/text()')
                            jg = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"价格")]/../span[2]/text()')
                            yxq = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"有效期")]/../span[2]/text()')
                            atc = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"ATC编码")]/../span[2]/text()')
                            jgfj = sel.xpath('//div[@class="drugdiv"]/span[contains(text(),"监管分级")]/../span[2]/text()')

                            list.append(ypcf)
                            list.append(syz)
                            list.append(yfyl)
                            list.append(ywgl)
                            list.append(yyrq)
                            list.append(fda)
                            list.append(ywxhzy)
                            list.append(compay)
                            list.append(jx)
                            list.append(gg)
                            list.append(jg)
                            list.append(yxq)
                            list.append(atc)
                            list.append(jgfj)
                            data.append(list)
                            # print(list)

        # 根据科室分开导出到excel
        download_excel(data,keshi)

def download_excel(data,keshi):
    print('keshi:' + keshi)
    print('dataSize:' + str(len(data)))
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet(keshi)
    col = ['药品大类', '科室','药品标签', '药品名称1', '药品名称2', '药品名称3', '药品英文名称', '药品成分', '适应症', '用法用量', '药物过量', '用药人群','FDA妊娠药物分级','药物相互作用','生产企业','剂型','规格','价格','有效期','ATC编码','监管分级']
    for k in range(0, 21):
        sheet.write(0, k, col[k])
    for i in range(0, len(data)):
        new_data = data[i]
        for j in range(0, 21):
            sheet.write(i + 1, j,new_data[j])
    workbook.save('D:\Python\yiku\医库-'+keshi+'.xls')
    print(keshi + '保存完毕')


if __name__ == '__main__':
    get_data()
    #download_excel(data)
