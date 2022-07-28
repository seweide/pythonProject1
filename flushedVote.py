import pyppeteer
import requests
from requests.cookies import RequestsCookieJar
import requests as requestsModule
import urllib.request
import json as js
import xlwt
from bs4 import BeautifulSoup
import re, os,time
import asyncio
import xlsxwriter
import zipfile
from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup
import json as js

url_detail = 'https://icd11.pumch.cn/api/services/app/MMS/GetMMSDetailFromId'
title_arr = []
type_arr = ['1','2','3']
openid_arr = ['885A03C84BA5CC8B450D058F8708212D8A731BEB',
              '5963574F1FFA09F1DF88F159000FBF03B797B07D',
              '3B301C0A2271670D06B29EB04E969A7EC8C7047B',
              ]

async def get_html(url):
    browser = await pyppeteer.launch(headless=True, args=['--no-sandbox'])
    page = await  browser.newPage()
    page.setCookie('6EE00F4AB148E31C2FB7CC0CF09A5631')
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

def request_url_get(s,url):
    suffix_1 = '&orderid=3&mainid=1553457576&openid='
    suffix_2 = '&istrue=0&_=1624358179777'
    #自定义cookies
    # jar = s.cookies.RequestsCookieJar()
    # jar.set('JSESSIONID', '6EE00F4AB148E31C2FB7CC0CF09A5631', domain='jia3.tmsf.com', path='/cookies')
    # cookies = {'JSESSIONID': '6EE00F4AB148E31C2FB7CC0CF09A5631'}
    # cookie_jar = RequestsCookieJar()
    # cookie_jar.set('JSESSIONID', '6EE00F4AB148E31C2FB7CC0CF09A5631', path='/', domain='jia3.tmsf.com')
    # r = s.get("http://jia3.tmsf.com",cookies=cookie_jar)
    # print(r.cookies)

    # s = requests.Session()
    # s.cookies.set('JSESSIONID', '6EE00F4AB148E31C2FB7CC0CF09A5631', path='/', domain='jia3.tmsf.com')
    # print(s.cookies.get('JSESSIONID'))

    for openid in openid_arr:
        for i in range(0, len(type_arr)):
            print('type:'+type_arr[i])
            for num in range(0,10):
                url = url + suffix_1 + type_arr[i] + openid + suffix_2
                re = s.get(url, stream=True)
                # re = get_html(url)
                print(type(requests.cookies))
                text_str = re.text
                print('text_str+'+text_str)
                js_test = js.loads(text_str)
                result = js_test['codetype']
                if result == 200:
                    print('投票'+num+'次成功')


def sendCheckcode(url,telphone):
    mem_sendCheckcode_url = url+telphone+'&checkcheckcode=6293&uuid=123&_=1624355900204'
    s = requests.session()
    res = s.get(mem_sendCheckcode_url, stream=True)
    text_str = res.text
    js_test = js.loads(text_str)
    flag = js_test['flag']
    if flag == 'true':
        codetype = js_test['codetype']
        print(codetype)
        msg = js_test['msg']
        print(msg)
    else:
        print(js_test['msg'])

def LoginByGet(url,telphone,code):
     # 登录Url
     mem_loginwithtelphone_url = url+telphone+'&checkcode='+code+'&token=123&_=1624355738797'
     s=requests.session()
     # 先打印一下，此时一般应该是空的。
     res = s.get(mem_loginwithtelphone_url, stream=True)
     print(s.cookies.get_dict())
     res.encoding = 'utf-8'
     c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
     c.set('JSESSIONID', '18B3EA637C620E39876CA567DE8CF07E')
     s.cookies.update(c)
     print(s.cookies.get_dict())
     text_str = res.text
     js_test = js.loads(text_str)
     flag = js_test['flag']
     if flag == 'true':
         codetype = js_test['codetype']
         print(codetype)
     else:
         print(js_test['msg'])
     return s

def GetCookie(url):
    s=requests.session()
    print(s.cookies.get_dict())#先打印一下，此时一般应该是空的。
    res=s.get(url,stream=True)
    text_str = res
    c=requests.cookies.RequestsCookieJar()#利用RequestsCookieJar获取
    c.set('cookie-name','cookie-value')
    s.cookies.update(c)
    print(s.cookies.get_dict())

if __name__ == '__main__':
    telphone = '15618747163'
    code = '567652'
    #获取验证码
    mem_sendCheckcode_url = 'http://jia3.tmsf.com/tmj3/mem_sendCheckcode.jspx?telphone='
    # sendCheckcode(mem_sendCheckcode_url, telphone)

    #登录Url
    mem_loginwithtelphone_url = 'http://jia3.tmsf.com/tmj3/mem_loginwithtelphone.jspx?telphone='
    # s =LoginByGet(mem_loginwithtelphone_url,telphone,code)
    #刷票
    s = requests.session()
    # 先打印一下，此时一般应该是空的。
    print(s.cookies.get_dict())
    c = requests.cookies.RequestsCookieJar()  # 利用RequestsCookieJar获取
    c.set('JSESSIONID', '18B3EA637C620E39876CA567DE8CF07E')
    s.cookies.update(c)
    print(s.cookies.get_dict())
    festival_vote_url = 'http://jia3.tmsf.com/hzf/festival_vote.jspx?type='
    data = request_url_get(s,festival_vote_url)