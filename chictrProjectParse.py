import pyppeteer
import xlwt
import requests
from bs4 import BeautifulSoup

excel_title_arr =['注册号：','注册题目：','研究课题的正式科学名称：','征募研究对象情况：'
    ,'研究所处阶段：','研究疾病：',	'研究目的：',	'试验分类：'	,'研究设计：'
    ,	'随机方法：',	'试验范围：',	'盲法：',	'年龄范围：',	'性别：',	'目标人数国内：'
    ,	'目标人数国际：',	'纳入标准：',	'排除标准：',	'药物名称：',	'药物类型：'
    ,	'试验药：',	'试验药用法用量：',	'对照药：',	'对照药用法用量：',	'研究负责人：'
    ,	'研究负责人职称：',	'研究负责人单位：',	'研究负责人电子邮件：',	'研究负责人电话：'
    ,	'研究负责人邮政编码：',	'研究负责人通讯地址：',	'研究实施负责（组长）单位：','Leading PI：'
    ,	'参与机构名称：',	'首次伦理时间：',	'首次公示时间：',	'申办方名称：',	'申办方联系人：'
    ,	'申办方联系电话：',	'申办方联系地址：',	'申办方邮箱：',	'研究实施时间：']

column_arr = []
project_id_All_arr = []

page_url = 'https://www.chictr.org.cn/searchproj.aspx?title=&officialname=&subjectid=&secondaryid=&applier=&studyleader=&ethicalcommitteesanction=&sponsor=&studyailment=&studyailmentcode=&studytype=0&studystage=0&studydesign=0&minstudyexecutetime=&maxstudyexecutetime=&recruitmentstatus=0&gender=0&agreetosign=&secsponsor=&regno=&regstatus=0&country=&province=&city=&institution=&institutionlevel=&measure=&intercode=&sourceofspends=&createyear=0&isuploadrf=&whetherpublic=&btngo=btn&verifycode=&page='

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

def request_url_get(url, false=None):
    re = requests.get(url)
    text_str = re.text
    districtSoup = BeautifulSoup(text_str)
    table_list = districtSoup.find("table", class_="table_list")
    a_list = districtSoup.findAll("a")
    check_str = 'showproj.aspx?proj'
    project_id_arr = []
    for link in a_list:
        if check_str in link.get('href'):
            print(link.get('href'))
            id = link.get('href').split('=')[1]
            project_id_arr.append(id)
            project_id_All_arr.append(id)


    if len(project_id_arr) > 1:
        for id in project_id_arr:
            print("id:" + id)
            getProjectDetail(id)
    # return return_arr

# 请求Url，返回html
def url_open(url):
    proxy = '110.87.248.151:8080'
    proxies = {
        'http': 'http://' + proxy,
        'https': 'http://' + proxy
    }
    # re = requests.get(url=url, proxies=proxies)
    re = requests.get(url)
    text_str = re.text
    districtSoup = BeautifulSoup(text_str)
    return districtSoup

def getProjectDetail(id):
    row_arr = []
    url = "https://www.chictr.org.cn/hvshowproject.aspx?id=" + id
    data = url_open(url)
    body_arr = data.find("body")
    child = body_arr.find('div', class_="ProjetInfo_title")
    title_arr = []

    for body in body_arr:
        if isinstance(body, str):
            continue
        # child2 = body.find('div', class_="ProjetInfo_ms")
        child2_list = body.contents
        if len(child2_list) > 0:
            for i in range(0, len(child2_list)):
                tbody = child2_list[i].find("tbody")
                if tbody is not None:
                    if isinstance(tbody, str):
                        print(tbody)
                    elif isinstance(tbody, int):
                        continue
                    else:
                        for link in tbody:
                            if isinstance(link, str):
                                continue
                            left_title = link.find("td", class_="left_title")
                            if left_title is not None:
                                td_list = link.contents
                                # True 就是整数 1，False 就是整数 0。
                                isVal = 0
                                for j in range(0, len(td_list)):
                                    p = td_list[j].find("p")
                                    if isinstance(p, str):
                                        print("p:"+p)
                                    elif isinstance(p, int):
                                        continue
                                    elif p is None:
                                        if isVal == 1:
                                            value = td_list[j].text
                                            value = value.replace("\n", "")
                                            value = value.replace("\r", "")
                                            value = value.strip()
                                            row_arr.append(value)
                                            isVal = 0
                                            print("str:" + value)
                                        else:
                                            continue
                                    elif p is not None:
                                        p_arr = p.contents
                                        for x in range(0, len(p_arr)):
                                        # for pda in p:
                                            if isinstance(p_arr[x], str):
                                                pda = p_arr[x].replace("\n", "")
                                                pda = pda.replace("\r", "")
                                                pda = pda.strip()
                                                if pda in excel_title_arr:
                                                    print("title:" + pda)
                                                    isVal = 1
                                                    title_arr.append(pda)
                                                elif isVal == 1:
                                                    print("value:" + pda)
                                                    row_arr.append(pda)
                                                    isVal = 0
                                                else:
                                                    continue
    temp_data = []
    if len(title_arr) > 0 and len(row_arr) > 0:
        for i in range(0,len(excel_title_arr)):
            if excel_title_arr[i] in title_arr:
                for j in range(0, len(title_arr)):
                    if title_arr[j] == excel_title_arr[i]:
                        temp_data.append(row_arr[j])
            else:
                temp_data.append("null")


    if len(temp_data) > 0:
        column_arr.append(temp_data)



def download_excel(data):
    workbook = xlwt.Workbook('utf-8')
    sheet = workbook.add_sheet('研值圈_数据字典整理_项目')
    col = excel_title_arr
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

    workbook.save('/Users/heweiwen/Downloads/work/work/Python/研值圈_数据字典整理_项目.xls')
    print('保存完毕')

def getProjectListPage():
    for i in range(1, 4):
        print("当前页码："+str(i))
        url = page_url + str(i)
        request_url_get(url)
        # 打印id
        if len(project_id_All_arr) > 0:
            print(project_id_All_arr)

    # 执行导出
    download_excel(column_arr)

if __name__ == '__main__':
    url = 'https://www.chictr.org.cn/searchproj.aspx'
    # data = request_url_get(url)
    # getProjectDetail('171070')
    getProjectListPage()


    # def get_proxy(self):
    #     proxy_arr = [
    #         '110.87.248.151:8080',
    #         '175.175.152.44:8888',
    #         '121.61.163.116:9999',
    #         '220.184.160.92:8080',
    #         '114.106.157.71:9999',
    #         '180.120.170.62:8080',
    #     ]
    #     proxy = '113.237.244.117:9999'
    #     proxies = {
    #         'http': 'http://' + proxy,
    #         'https': 'http://' + proxy
    #     }
    #
    #     return proxies
    #
    #
    # def send_post(self, url, data):
    #     '''
    #     发送post请求
    #     '''
    #     # res=requests.post(url=url,data=data)
    #     proxies = self.get_proxy()
    #     res = requests.post(url=url, data=data, proxies=proxies)
    #     return res
    #
    #
    # def send_get(self, url, data):
    #     '''
    #     发送get请求
    #     '''
    #     # res=requests.get(url=url,params=data)
    #     proxies = self.get_proxy()
    #     res = requests.get(url=url, params=data, proxies=proxies)
    #     return res
    #
    #
    # def send_method(self, method, url, data):
    #     '''
    #     执行方法，传递method、url、data
    #     '''
    #     if method == 'post':
    #         res = self.send_post(url, data).json()
    #     else:
    #         res = self.send_get(url, data).json()
    #     try:
    #         res = json.dumps(res, indent=4)
    #     except:
    #         print('编码成json字符串报错')
    #     return res