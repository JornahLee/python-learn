#! /usr/bin/python3


# 字符串下标从0开始
def fun2():
    s = 'abcde '
    print(s * 5)  # 输出五次s
    print(s[1:])  # 1~结尾
    print(s[:5])  # 起点 ~ 5
    return


# 列表 List,有序集合
# 下标左闭右开

def fun1():
    li = ['1', '2', '3', '4', '5']
    print(li[0:5:2])  # 下标0-5的元素，步长为2
    return


def list_contact(list1, list2):
    return list1 + list2


def test_str():
    for i in '123':
        print(i)
        print(type(i))
    return


# 序列
def test_list_contact():
    list1 = ['1', '2', '3', '4', '5']
    list2 = ['1', '2', '3', '4', '5']
    print(list_contact(list1, list2))
    return


# 字典，hashmap,使用 a={}创建空字典
def test_dict():
    dic = {"1": 1, "2": 2}
    print(type(dic))
    dic["1"] = ['1', '2', '3', '4', '5']
    res = dic["1"]
    print(res)
    print(dic.keys())
    print(dic.values())
    print(type(dic))
    print(type(dic.keys()))
    print(type(dic.values()))
    for k, v in dic.items():
        print('k,v=' + k + ',' + str(v))
    return


# 集合，无重复元素
# 如果要创建一个空集合，你必须用 set() 而不是 {} ；后者创建一个空的字典，
def test_collection():
    collection1 = {'100', '3', '1', '2', '2', '3', '4', '5'}
    print(collection1)
    return


# 同时遍历两个或更多的序列
def test_zip():
    questions = ['name', 'quest', 'favorite color']
    answers = ['lancelot', 'the holy grail', 'blue']
    for q, a in zip(questions, answers):
        print('What is your {0}?  It is {1}.'.format(q, a))


# 反向遍历
def test_reversed():
    for i in reversed(range(1, 10, 2)):
        print(i)


# 排序
def test_sort():
    li = [4, 51, 6, 7, 88, 1, 2, 4, 66]
    for i in sorted(li):
        print(i)
    print("----str sorted")
    li = ["4", "51", "6", "7", "88", "1", "2", "4", "66"]
    for i in sorted(li):
        print(i)
    print("----str2 sorted")
    li = ["a4", "a51", "6", "7", "88", "1a", "2", "4", "66"]
    for i in sorted(li):
        print(i)


# Python数据类型转换 , 见https://www.runoob.com/python/python-variable-types.html
def test_calc():
    a = 100
    b = 2
    res = a ** b  # a的b次幂
    print(res)
    res = a // b  # 取整除 - 返回商的整数部分（向下取整）
    print(res)
    res = a / b  # 取整除 - 返回商的整数部分（向下取整）
    print(res)
    return


def test_bit_calc():
    a = 1  # 001
    b = 5  # 101
    res = a & b
    print(res)
    res = a | b
    print(res)
    res = a ^ b
    print(res)
    res = ~a
    print(res)
    return


# Python逻辑运算符：  and  or  not (非0（非空）则为真,)  ， python 并不支持 switch 语句
def test_logic_calc():
    a = [1, 2]
    b = 2
    res = a or b
    print(res)
    print(1 or 2)
    print(1 and 2)
    print(not 0)
    print(not 1)
    return


# Python成员运算符: in , not in
def test_member_calc():
    a = [1, 2, 3]
    if 1 in a:
        print(str(1) + " in")
    if 10 not in a:
        print(str(10) + " not in ")
    return


# Python身份运算符 身份运算符用于比较两个对象的存储单元（是不是同一个引用）: is , is not
def test_reference():
    a = "1"
    b = "1"
    print(a is b)
    c = 1
    d = [1, 2]
    print(c is d[0])
    d1 = {}
    d2 = {}
    print(d1 is d2)
    l1 = {}
    d = l2 = {}
    print(l1 is l2)
    print(type(a))
    print(type(c))
    print(type(True))
    return


def test_cycle():
    dict = {1: 1, 2: 2, 3: 3}
    for k in dict.values():
        print(type(k))
        print(k)
    for k in dict.keys():
        print(type(k))
        print(k)

    fruits = ['banana', 'apple', 'mango']
    for index in range(len(fruits)):
        print('当前水果 :', fruits[index])
    return


def test_loop():  # else 中的语句会在循环正常执行完（即 for 不是通过 break 跳出而中断的）的情况下执行
    for i in range(0, 100):
        print(i)
        break
    else:
        print(200)


def test_itr():
    li = range(0, 100)
    itr = iter(li)
    for x in itr:
        print(x)


def test_itr2():
    li = range(0, 100)
    itr = iter(li)
    while True:
        try:
            print(next(itr))
        except StopIteration:
            break


if __name__ == '__main__':
    test_sort()

# 常用函数: str() len() type() range()
# Python pass 是空语句，是为了保持程序结构的完整性。
# pass 不做任何事情，一般用做占位语句。
# 类型转换
# int(x [,base ])         将x转换为一个整数
# long(x [,base ])        将x转换为一个长整数
# float(x )               将x转换到一个浮点数
# complex(real [,imag ])  创建一个复数
# str(x )                 将对象 x 转换为字符串
# repr(x )                将对象 x 转换为表达式字符串
# eval(str )              用来计算在字符串中的有效Python表达式,并返回一个对象
# tuple(s )               将序列 s 转换为一个元组
# list(s )                将序列 s 转换为一个列表
# chr(x )                 将一个整数转换为一个字符
# unichr(x )              将一个整数转换为Unicode字符
# ord(x )                 将一个字符转换为它的整数值
# hex(x )                 将一个整数转换为一个十六进制字符串
# oct(x )
