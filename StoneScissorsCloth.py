import random

# 石头
stone = 1

# 剪刀
scissors = 2

# 布
cloth = 3

def getStone():
    print('获取石头')

def getScissors():
    print('获取剪刀')

def getCloth():
    print('获取布')

def rock_paper_scissors(s1:str,s2:str)->str:
    # 最基础的复合条件判断语句
    if s1 == s2:
        ans = "平局"
    elif (s1 == "剪刀" and s2 == "布" or s1 == "石头" and s2 == "剪刀" or s1 == "布" and s2 == "石头"):
        ans = "甲胜"
    else:
        ans = "乙胜"
    return ans

def rock_paper_scissors2(s1:str,s2:str)->str:
    # 用字典存储各种手法的天敌关系
    R= {"剪刀":"石头", "石头":"布", "布":"剪刀"}
    if s1 == s2:
        ans = "平局"
    elif s1 == R[s2]:
        # s1是s2的天敌
        ans = "甲胜"
    else:
        ans = "乙胜"
    return ans

def rock_paper_scissors3(s1:str,s2:str)->str:
    # 用字典存储各种手法的序号、数值差对应的结果，再直接返回结果
    num = {"剪刀":1, "石头":2,"布":3}
    ans = {0:"平局", 1:"甲胜", -2:"甲胜", -1:"乙胜", 2:"乙胜"}
    return ans[num[s1] - num[s2]]

if __name__ == '__main__':
    print('====石头剪刀布====')

    getCloth()
    getStone()
    getScissors()

    print('----结束----')