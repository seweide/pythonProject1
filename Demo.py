from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby #itertool还包含有其他很多函数，比如将多个list联合起来。。
import pandas as pd
import pandas as df

lst = [2, 8, 11, 25, 43, 6, 9, 29, 51, 66]
d1 = {'name': 'zhangsan', 'age': 20, 'country': 'China'}
d2 = {'name': 'wangwu', 'age': 19, 'country': 'USA'}
d3 = {'name': 'lisi', 'age': 22, 'country': 'JP'}
d4 = {'name': 'zhaoliu', 'age': 22, 'country': 'USA'}
d5 = {'name': 'pengqi', 'age': 22, 'country': 'USA'}
d6 = {'name': 'lijiu', 'age': 22, 'country': 'China'}

def test():
    df1 = df[['一级分类', '二级分类', '7天点击量', '订单预定']]
    for (key1, key2), group in df1.groupby(['一级分类', '二级分类']):
        print(key1, key2)
        print(group)

def test1():

    lst = [d1, d2, d3, d4, d5, d6]

    # 通过country进行分组：

    lst.sort(key=itemgetter('country'))  # 需要先排序，然后才能groupby。lst排序后自身被改变
    lstg = groupby(lst, itemgetter('country'))
    # lstg = groupby(lst,key=lambda x:x['country']) 等同于使用itemgetter()

    for key, group in lstg:
        for g in group:  # group是一个迭代器，包含了所有的分组列表
            print(key,g)

def test2():
    def gb(num):
        if num <= 10:
            return 'less'
        elif num >= 30:
            return 'great'
        else:
            return 'middle'


    for (k,g) in groupby(sorted(lst),key=gb):
        print(k, list(g))


if __name__ == '__main__':
    test();
    # test1();
    # test2();
    print('Hallo,你好！Python')