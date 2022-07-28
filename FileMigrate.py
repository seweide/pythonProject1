import pyppeteer
import requests
import asyncio
import random
import json
import re, os,time
import shutil
import asyncio
from pyppeteer import launch
from lxml import etree
import xlwt
from pyquery import PyQuery as pq
import ssl
import logging
import sys
import docx
from docx import opc
from docx.opc.constants import CONTENT_TYPE as CT
from docx.package import Package
import zipfile
from read import read
import pkgutil
import xlsxwriter
import numpy as np

def migrate():
    file_path = os.path.join(os.getcwd(), '国家药品监督管理局说明书/')
    new_file_path = os.path.join(os.getcwd(), '无法识别/')
    #获取 需要迁移文档名
    notfiles = [
        'gyzzH10930061sms.doc',
        'gyzzH10930061sms.doc',
        'gyzzH14023577sms.doc',
        'gyzzH20203021sms.doc',
        'gyzzH19993034sms.doc',
        'gyzzH20100151sms.doc',
        'gyzzH20113281sms.doc',
        'gyzzH20080241sms.doc',
        'gyzzH20203551sms.doc',
        'gyzzH20203685sms.doc',
        'gyzzH20194080sms.doc',
        'gyzzH20203048sms.doc',
        'gyzzH20113231sms.doc',
        'gyzzH20163163sms.doc',
        'gyzzH20057288sms.doc',
        'gyzzH20010677sms.doc',
        'gyzzH20093447sms.doc',
        'gyzzH20130115sms.doc',
        'gyzzH20130064sms.doc',
        'gyzzH20080371sms.doc',
        'gyzzH20203569sms.doc',
        'gyzzH20000094sms.doc',
        'gyzzH19993035sms.doc',
        'gyzzH20110051sms.doc',
        'gyzzH20010571sms.doc',
        'gyzzH20055812sms.doc',
        'gyzzH20203403sms.doc',
        'gyzzH20061218sms.doc',
        'gyzzH20058740sms.doc',
        'gyzzH20203043sms.doc',
        'gyzzH20103327sms.doc',
        'gyzzH20066717sms.doc',
        'gyzzH20065120sms.doc',
        'gyzzH20203395sms.doc',
        'gyzzH20058070sms.doc',
        'gyzzH20120021sms.doc',
        'gyzzH20070319sms.doc',
        'gyzzH20010575sms.doc',
        'gyzzH20051067sms.doc',
        'gyzzH20046056sms.doc',
        'gyzzH20203082sms.doc',
        'gyzzH12020224sms.doc',
        'gyzzH20193351sms.doc',
        'gyzzH20084486sms.doc',
        'gyzzH20203192sms.doc',
        'gyzzH13020787sms.doc',
        'gyzzH20057289sms.doc',
        'gyzzH20060666sms.doc'
    ]
    # 遍历文件夹
    files = []
    for root, dirs, files in os.walk(file_path):
        print(files)
        files = files
        i = 0
    for file_name in files:
        if file_name in notfiles:
            full_path = os.path.join(file_path, file_name)  # 将文件目录与文件名连接起来，形成原来完整路径
            des_path = os.path.join(new_file_path, file_name)   # 目标路径
            # 移动文件到目标路径
            shutil.move(full_path, des_path)
if __name__ == '__main__':
    print('文件迁移-开始')
    migrate()
    print('完成')