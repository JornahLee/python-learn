#!/usr/bin/python
# -*- coding: UTF-8 -*-


# 常用打开文件 模式
def usual_mode():
    """
    r 读， 指针在头部
    w 写？ 创建合适些，指针在头部
    a 文末追加， 指针到末尾
    + 可读可写, 需搭配 r w a 使用
    文本模式(默认)/二进制模式 t/b

    例：
    写入二进制文件 如excel：  wb+
    读写文本： r+（文件存在）, w+(文件不存在)
    """
    pass


# 读取文件
def read_text_file():
    # 读取所有行
    with open("filename.txt") as file:
        all_line = file.read()
        print(all_line, end='')
    print("-----------")
    # 逐行读取 方法1
    with open("filename.txt") as file:
        for line in file:
            print(line, end='')
    print("-----------")
    # 逐行读取 方法2
    with open("filename.txt") as file:
        line = file.readline()  # 调用文件的 readline()方法
        while line:
            print(line, end='')  # 在 Python 3 中使用
            line = file.readline()
    pass


# 写入文本到文件
def write_file():
    with open('./test.txt', 'w+') as file:
        file.write('test')
        # 不会自动添加换行符，只会逐个输出数组中的内容
        file.writelines(['line1', 'line2'])
    pass


if __name__ == '__main__':
    write_file()
    # read_text_file()

    pass
