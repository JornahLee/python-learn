# 字符串操作
# 定义 '' "" """ """
# 打印字符串
# 拼接 截取 拆分
# 格式化输出 字符串中插入变量
# 判断相等  判空 字符串匹配
# 正则

def test():
    # 定义字符串 '' 和 ""基本通用
    str1 = ''
    str2 = ""
    # 支持多行的字符串，无需转义字符
    str3 = """
        sdfsdf 
        sfsdf"""
    print(str1)
    print(str2)
    print(str3)

    # 字符串模板输出变量
    what = 123
    my_str = f"this is {what + 1}"
    # 还有一种%s方式，并不好用
    strn = "%s %s" % ('1', '2')
    print(strn)
    my_str2 = "woshi {0}".format('haha')
    # 格式化字符串
    print(my_str)
    print(my_str2)

    # 截取字符串
    # 0代表第一个元素索引, 负数代表倒数第一个元素, 不写则代表第一个或最后一个
    # 下标是左闭右开
    # 感觉py字符串就是  字符list，所以和list相关运算符都一样
    print('sub str 123'[:-1])  # sub str 12
    print('sub str 123'[0:])  # sub str 123
    print('sub str 123'[1:2])  # u
    # 可指定步长
    print('123456789'[::2])  # 13579

    # 拆分字符串
    # 不加参数，则以whitespace拆分
    print('1 2 3\t4 '.split())  # ['1', '2', '3', '4']
    # 指定separator
    print('1 2 3 4 '.split(' '))  # ['1', '2', '3', '4', '']
    # 指定最大分割次数
    print('1 2 3 4 '.split(' ', 1))  # ['1', '2 3 4 ']
    # 指定分割方向 从右开始
    print('1 2 3 4 '.rsplit(' ', 1))  # ['1 2 3 4', '']

    # 字符串比较
    print('1' == '12')  # false == 比较值
    print('1' in '12')  # true in 其实表包含，那字符串去目标集合遍历
    a = ''
    b = ''
    print(a is b)  # true 判断两个对象的内存地址是否一样

    # 字符串判空
    print('\t \n'.isspace())  # True isBlank
    print(len('') == 0)  # True isEmpty
    print('' is None)  # False isNone
    pass


if __name__ == '__main__':
    test()
