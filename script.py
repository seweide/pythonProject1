# script.py
# from mitmproxy import http
#
# def request(flow: http.HTTPFlow) -> None:
# 	# 将请求新增了一个查询参数
#     flow.request.query["mitmproxy"] = "rocks"
#
# def response(flow: http.HTTPFlow) -> None:
# 	# 将响应头中新增了一个自定义头字段
#     flow.response.headers["newheader"] = "foo"
#     print(flow.response.text)


import json
import csv


def response(flow):
    url = 'https://shopping.ele.me/h5/mtop.venus.shopcategoryservice.getcategorydetail'
    if flow.request.url.startswith(url):  # 筛选出需要的接口进行分析
        text = flow.response.text  # 接口返回的内容
        res_dict = json.loads(text)  # 字符串转字典
        data = res_dict['data']['data'][0]['foods']  # 获取商品内容

        csvfile = open('test.csv', 'a')  # 处理后的数据写入csv文件
        csv_wri = csv.writer(csvfile)

        for food in data:  # 遍历商品内容
            cate2id = food['categoryIds'][0]  # eleme平台对应的二级类目id
            currentPrice = food['currentPrice']  # 单位是元
            defaultSaleUnit = food['defaultSaleUnit']  # 销售规格
            leftNum = food['leftNum']  # 库存
            monthSell = food['monthSell']  # 月销量
            name = food['name']  # 商品名
            photos = food['photos']  # 商品图片
            upc = food['upc']  # 商品upc

            csvItem = [upc, name, defaultSaleUnit, currentPrice, leftNum, monthSell, cate2id, photos]
            csv_wri.writerow(csvItem)

        csvfile.close()
