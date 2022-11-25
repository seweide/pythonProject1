import random
import requests
import time
import json as js

# 发布动态imgs图片集合
imgs_arr = [
    '2021-09-07/4732_1-20210907140846.jpg',
    '2021-09-17/589_2-20210917100046.jpg',
    '2021-09-17/589_1-20210917100046.jpg',
    '2021-09-17/11019_1-20210917102750.jpg',
    '2021-09-07/4732_1-20210907140846.jpg',
    '2021-09-07/589_1-20210907141240.jpg',
    '2021-09-18/10996_1-20210918091755.png',
    '2021-09-12/651_1-20210912091104.jpg',
    '2021-09-11/651_1-20210911074915.jpg',
    '2021-09-10/4732_1-20210910102305.jpg',
    '2021-09-10/651_1-20210910092025.jpg',
    '2021-09-10/2256_1-20210910091836.jpg',
    '2021-09-09/651_1-20210909093742.jpg',
    '2021-09-08/6034_1-20210908000509.jpg',
    '2021-09-06/651_1-20210906121534.jpg',
    '2021-09-06/651_2-20210906121534.jpg',
    '2021-09-05/651_1-20210905081709.jpg',
    '2021-09-04/651_1-20210904075816.jpg',
    '2021-09-03/651_1-20210903112413.jpg',
    '2021-09-02/589_1-20210902095725.jpg',
    '2021-09-01/589_1-20210901190542.jpg',
    '2021-09-01/5047_1-20210901090836.jpg',
    '2021-08-31/2256_1-20210831095511.jpg',
    '2021-08-29/909_1-20210829212140.jpg',
    '2021-08-24/10473_1-20210824211846.jpg',
    '2021-08-20/2256_1-20210820172546.jpg',
    '2021-08-20/909_1-20210820081013.jpg',
    '2021-08-19/3859_1-20210819005823.jpg',
    '2021-09-07/4732_1-20210907140846.jpg',
    '2021-09-18/417_1-20210918073917.jpg',
    '2021-09-18/417_4-20210918073917.jpg',
    '2021-08-25/7261_1-20210825075352.jpg',
    '2021-09-10/909_1-20210910005127.jpg',
    '2021-09-14/11222_1-20210914035734.jpg',
    '2021-09-12/7402_1-20210912104238.jpg',
    '2021-09-12/7402_4-20210912104238.jpg',
    '2021-09-09/10385_1-20210909085842.png',
    '2021-09-13/417_1-20210913074005.jpg',
    '2021-09-13/417_2-20210913074005.jpg',
    '2021-09-18/10487_1-20210918123528.jpg',
    '2021-09-18/1098_1-20210918105559.jpg',
    '2021-09-18/724_4-20210918102317.jpg',
    '2021-09-18/724_1-20210918102318.jpg',
    '2021-09-17/7287_1-20210917223306.jpg',
    '2021-09-17/7287_3-20210917223306.jpg',
    '2021-09-17/7287_2-20210917223306.jpg',
    '2021-09-17/1098_1-20210917100614.jpg',
    '2021-09-17/2256_1-20210917093923.jpg',
    '2021-09-17/2145_1-20210917000520.jpg',
    '2022-02-09/10941_1-20220209220121.jpg',
    '2022-02-09/589_1-20220209165938.jpg',
    '2022-02-09/5799_1-20220209102152.jpg',
    '2022-02-09/5799_3-20220209102152.jpg',
    '2022-02-09/5799_2-20220209102152.jpg',
    '2022-02-11/5971_1-20220211091139.jpg',
    '2022-02-11/5971_2-20220211091139.jpg',
    '2022-02-13/5799_1-20220213103727.jpg',
    '',
    '2021-09-07/589_1-20210907141240.jpg'
]

# 评论+发布新动态集合
content_arr = [
        '天行健，君子以自强不息；地势坤，君子以厚德载物。——《周易》',
        '知者不惑，仁者不忧，勇者不惧。——《论语》',
        '得道者多助，失道者寡助。——《孟子》',
        '积善之家，必有余庆；积不善之家，必有余殃。——《周易》',
        '物有本末，事有终始。知所先后，则近道矣。——《大学》',
        '学而时习之，不亦说乎？有朋自远方来，不亦乐乎？人不知而不愠，不亦君子乎？——《论语》',
        '君子藏器于身，待时而动。——《周易》',
        '君子喻于义，小人喻于利。——《论语》',
        '鱼，我所欲也，熊掌，亦我所欲也；二者不可得兼，舍鱼而取熊掌者也。生，亦我所欲也；义，亦我所欲也；二者不可得兼，舍生而取义者也。——《孟子》',
        '学而不思则罔，思而不学则殆。——《论语》',
        '天下同归而殊途，一致而百虑。——《周易》',
        '见善则迁，有过则改。——《周易》',
        '穷则变，变则通，通则久。——《周易》',
        '居上位而不骄，在下位而不忧。——《周易》',
        '三人行，必有我师焉。择其善者而从之，其不善者而改之。——《论语》',
        '中国名言警句摘抄大全，好学近乎知，力行近乎仁，知耻近乎勇。——《中庸》',
        '天命之谓性，率性之谓道，修道之谓教。——《中庸》',
        '君子和而不同，小人同而不和。——《论语》',
        '博学之，审问之，慎思之，明辨之，笃行之。——《中庸》',
        '知之为知之，不知为不知，是知也。——《论语》',
        '二人同心，其利断金。同心之言，其臭如兰。——《周易》',
        '三思而后行。——《论语》',
        '三军可夺帅也，匹夫不可夺志也。——《论语》',
        '喜怒哀乐之未发，谓之中；发而皆中节，谓之和。中也者，天下之大本也；和也者，天下之达道也。致中和，天地位焉，万物育焉。——《中庸》',
        '老吾老，以及人之老；幼吾幼，以及人之幼。——《孟子》',
        '敖不可长，欲不可从，志不可满，乐不可极。——《礼记》',
        '富贵不能淫，贫贱不能移，威武不能屈，此之谓大丈夫。——《孟子》',
        '自诚明，谓之性；自明诚，谓之教。诚则明矣，明则诚矣。——《中庸》',
        '善不积，不足以成名；恶不积，不足以灭身。——《周易》',
        '度德而处之，量力而行之。——《春秋·左传》',
        '上不怨天，下不尤人。故君子居易以俟命，小人行险以徼幸。——《中庸》',
        '巧言令色，鲜矣仁！——《论语》',
        '吾日三省吾身：为人谋而不忠乎？与朋友交而不信乎？传不习乎？——《论语》',
        '古之欲明明德于天下者，先治其国。欲治其国者，先齐其家；欲齐其家者，先修其身；欲修其身者，先正其心；欲正其心者，先诚其意；欲诚其意者；先致其知；致在格物。——《大学》',
        '玉不琢，不成器；人不学，不知道。——《礼记》',
        '君子学以聚之，问以辩之，宽以居之，仁以行之。——《周易》',
        '所谓诚其意者，毋自欺也。如恶恶臭，如好好色，此之谓自谦。故君子必慎其独也。——《大学》',
        '故天将降大任于斯人也，必先苦其心志，劳其筋骨，饿其体肤，空乏其身，行拂乱其所为，所以动心忍性，曾益其所不能。——《孟子》',
        '劳心者治人，劳力者治于人；治于人者食人，治人者食于人；天下之通义也。——《孟子》',
        '岁寒，然后知松柏之后凋也！中国名言警句摘抄大全。——《论语》',
        '君子有诸己而后求诸人，无诸己而后非诸人。——《大学》',
        '玩人丧德，玩物丧志。——《尚书》',
        '敏而好学，不耻下问。——《论语》',
        '居安思危，思则有备，有备无患。——《春秋·左传》',
        '人谁无过？过而能改，善莫大焉。——《春秋·左传》',
        '差若毫厘，缪以千里。——《礼记》',
        '知者乐水，仁者乐山。知者动，仁者静。知者乐，仁者寿。——《论语》',
        '恻隐之心，仁之端也；羞恶之心，义之端也；辞让之心，礼之端也；是非之心，智之端也。——《孟子》',
        '多行不义，必自毙。——《春秋·左传》',
        '君子务本，本立而道生。——《论语》'
    ]
# 评论info集合
info_arr = [
        '666', 'AR YYDS', '早上好', '打卡', '签到', '今天天气清朗', '我来啦', '好好看', '不要太好看', 'AR娥罗多姿', '牛', '不要太好', '小众完美', '谁说AR保养贵',
        '666+1', 'AR+1 YYDS', '早上好+1', '打卡+1', '签到+1', '今天天气清朗+1', '我来啦+1', '好好看+1', '不要太好看+1', 'AR娥罗多姿+1', '牛+1',
        '不要太好+1', '小众完美+1', '谁说AR保养贵+1', '666+2', 'AR+2 YYDS', '早上好+2', '打卡+2', '签到+2', '今天天气清朗+2', '我来啦+2', '好好看+2',
        '不要太好看+2', 'AR娥罗多姿+2', '牛+2', '不要太好+2', '小众完美+2', '谁说AR保养贵+2', '666+3', 'AR+3 YYDS', '早上好+3', '打卡+3', '签到+3',
        '今天天气清朗+3', '我来啦+3', '好好看+3', '不要太好看+3', 'AR娥罗多姿+3', '牛+3', '不要太好+3', '小众完美+3', '谁说AR保养贵+3'
    ]

# uid集合
# uid_arr = [7650,724]
uid_arr = [589,4732,21056]
# uid_arr = [21056]

# 热门话题essid集合
essid_arr = [19584,19601]

# 话题Id集合
topid_arr = [18,28,33,35,39]

# 动态获取essid集合
essay_ids = []

# 动态获取img_urls集合
img_urls_arr = []
# 登录
def signIn(uid):
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/signIn?uid='+str(uid)
    r = requests.get(URL)
    print(r.text)
    print('登录成功')
# 签到
def myInfoToday(uid):
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/myInfoToday?uid='+str(uid)
    r = requests.get(URL)
    print(r.text)
    print('签到成功')

# 点赞
def thumbEss(uid,essid,type):
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/thumbEss?uid='+str(uid)+'&essid='+str(essid)+'&type='+str(type)
    r = requests.get(URL)
    print(r.text)
    print('点赞成功：')

# 发送来源-分享 type:1 分享, 3:分享
def sendScore(uid,type):
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/sendScore?uid='+str(uid)+'&type='+str(type)
    r = requests.get(URL)
    print(r.text)
    print('发送来源-分享-成功')

# 获得话题详情
def oneEssay(uid,essid):
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/oneEssay?uid='+str(uid)+'&essid='+str(essid)
    r = requests.get(URL)
    print(r.text)
    print('获得话题详情-成功'+str(essid))

# 查看话题
def collectEss(uid,essid):
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/collectEss?uid='+str(uid)+'&essid='+str(essid)+'&type=0'
    r = requests.get(URL)
    print(r.text)
    print('查看话题-成功'+str(essid))

# 最热列表
def getTopicEssay(uid,page,topid,type):
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/getTopicEssay?limit=20&page='+str(page)+'&uid='+str(uid)+'&topid='+str(topid)+'&type='+str(type)
    r = requests.get(URL)
    text_str = r.text
    js_test = js.loads(text_str)
    data = js_test['data']
    infos = data['info']
    if '' != infos:
        for i in range(0, len(infos)):
            essay_ids.append(infos[i]['id'])
            img_urls_arr.append(infos[i]['img_urls'])
    # 返回：
    return essay_ids

# 评论
def commentEss(uid,essid,isCycle):
    print('评论开始')
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/commentEss'
    if isCycle == 0:
        print('循环评论开始')
        uid_arr = [6811, 724, 7650, 589, 4732]
        for i in range(0, len(info_arr)):
            print('循环开始' + str(i))
            info = random.sample(info_arr, 1)
            # 随机uID
            uid = random.sample(uid_arr, 1)

            data = {
                'uid': (None, str(uid[0])),
                'essid': (None, essid),
                'commid': (None, ''),
                "info": (None, str(info[0]))
            }
            resp = requests.post(URL, files=data)
            print(resp.text)
            print('结束' + str(i))
            # 休息
            time.sleep(5)
    elif isCycle == 1:
        info = random.sample(info_arr, 1)
        data = {
            'uid': (None, str(uid)),
            'essid': (None, str(essid)),
            'commid': (None, ''),
            "info": (None, str(info[0]))
        }
        resp = requests.post(URL, files=data)
        print(resp.text)
        print('结束' + str(essid))


# 发布新动态
def addEssay(uid):
    print('发布最新动态')
    URL = 'https://miniprogram.alfaromeo.com.cn/apis/mini/v1/addEssay'
    content = random.sample(content_arr, 1)

    imgs_11 = random.sample(imgs_arr,1)
    imgs_22 = '["images/uploads/community/'
    imgs = imgs_22 + str(imgs_11[0]) + '"]'

    topid = random.sample(topid_arr,1)
    data = {
        'uid': (None, str(uid)),
        'topid': (None, str(topid[0])),
        'imgs': (None, str(imgs)),
        'title': (None, ''),
        "content": (None, str(content[0]))
    }
    resp = requests.post(URL, files=data)
    print(resp.text)
    print('发布新动态-成功')

# 执行
def taskInfo():
    # 循环执行两用户签到打卡
    for id in range(0,len(uid_arr)):
        # 登录
        signIn(uid_arr[id])
        # 签到
        myInfoToday(uid_arr[id])
        # 最热列表
        topid = random.sample(topid_arr, 1)
        essay_ids = getTopicEssay(uid_arr[id],1,topid[0],1)
        for i in range(0, len(essay_ids)):
            print('essay_id:' + str(essay_ids[i]))
        # 发布新动态
        addEssay(uid_arr[id])

        # 发送来源 - 分享
        for i in range(0, 3):
            sendScore(uid_arr[id], 1)


        # 循环5次 点赞，评论，浏览话题详情
        for i in range(0, 5):
            # 发送来源 - 阅读文章3
            sendScore(uid_arr[id], 3)
            # 评论
            commentEss(uid_arr[id], essay_ids[i], 1)
            # 查看话题
            collectEss(uid_arr[id], essay_ids[i])
            # 获得话题详情
            oneEssay(uid_arr[id], essay_ids[i])

        # 循环2次 点赞
        for i in range(0, 2):
            # 点赞
            thumbEss(uid_arr[id], essay_ids[i], 0)
            # 取消点赞
            thumbEss(uid_arr[id], essay_ids[i], 1)
            # 点赞
            thumbEss(uid_arr[id], essay_ids[i], 0)

if __name__ == '__main__':
    # 执行
    taskInfo()

    # 登录
    # signIn(724)
    # 签到
    # myInfoToday(724)

    # 发布新动态
    # addEssay(uid_arr[1])

    # 批量刷评论 (刷热门)
    # essid = 20728
    # uid = 7650
    # uid_arr = [6811, 724, 7650, 589, 4732]
    # commentEss(uid, essid, 0)
    # for i in range(0,len(uid_arr)):
    #     commentEss(uid_arr[i], essid, 0)

    # 刷点赞
    # for i in range(0,15):
    #     uid_ra = random.randint(1, 11376)
    #     # 点赞
    #     thumbEss(uid_ra, essid, 0)

    # 阅读文章 阅读文章3
    # for i in range(0, 3):
    #     sendScore(589, 1)

    # 最热列表
    # img_urls_arr = getTopicEssay(uid,1,22,1)
    # if [] != img_urls_arr:
    #     for i in range(0, len(img_urls_arr)):
    #         print('img_urls：'+ str(img_urls_arr[i]))

