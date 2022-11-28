import re

countAll = []


def openreadtxt(file_name):
    numCount = 0
    data = []
    file = open(file_name, 'r')  # 打开文件
    file_data = file.readlines()  # 读取所有行
    for row in file_data:
        # tmp_list = row.split(' ')  # 按‘，’切分每行的数据
        # tmp_list[-1] = tmp_list[-1].replace('\n',',') #去掉换行符
        # data.append(tmp_list)  # 将每行数据插入data中
        # N = re.compile(r'(\d+)-Main|-Side')
        # n = N.findall(row)
        number = re.findall("\d+", row)  # 输出结果为列表
        if number != []:
            temp = []
            for n in number:
                print('n:'+n)
                countAll.append(int(n))
                temp.append(int(n))
            tempNum = _sum(temp)
            numCount += tempNum
            print(tempNum)
        print(number)
    return numCount

def _sum(num):
    return sum(num)

if __name__ == "__main__":
    data = openreadtxt('Account.txt')
    # print('countAll:' +_sum(countAll))
    print(data)