#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os


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


# 键盘输入
def standard_input():
    # 标准输入
    str1 = input("input:")
    # 标准输出
    print(str1)


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


# 文件新建，删除，重命名； 目录创建
def file_operation():
    filename = "filename.txt"
    dir_name = "dirname"
    # 创建文件， 以w模式打开文件：创建文件, 如已存在则清空文件
    with open(filename, mode="w", encoding="utf-8"):
        pass
    os.rename(filename, 'rename.' + filename)
    os.remove('rename.' + filename)
    # 创建目录，父目录不存在会报错
    os.mkdir(dir_name)
    # 递归创建目录
    os.makedirs("sf/sdf")
    os.rmdir(dir_name)


# 判断文件或目录是否存在
def file_exists_test():
    folder_name = 'imgs'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


# 文件 大小 存储容量 易读
def human_size(byte_size: int):
    kb = byte_size / 1024
    if kb < 1000:
        # 保留小数点后两位， %号的使用
        return '%.2f' % kb + ' kb'
    mb = kb / 1024
    if mb < 1000:
        return '%.2f' % mb + ' mb'
    gb = mb / 1024
    if gb < 1000:
        return '%.2f' % gb + ' gb'


def recurse_path(path: str, processor, cur_depth=0, max_depth=999):
    if cur_depth > max_depth:
        return
    for item in os.scandir(path):
        if item.is_dir():
            recurse_path(item.path, processor, cur_depth + 1, max_depth)
            pass
        else:
            processor(item.path)


# 自己实现的目录递归， 其实别人已经有了os.walk()实现了。。。。
def test_path_recurse():
    recurse_path("/Users/macbook/logs", lambda x: print(x), max_depth=1)


# 递归遍历path
def test_walk():
    path = "/Users/macbook/logs"
    # return dir path,dir names,filenames
    for i in os.walk(path):
        for item in i[2]:
            print(os.path.join(path, item))


if __name__ == '__main__':
    # 测试递归遍历
    # test_path_recurse()
    # test_walk()
    # file_operation()
    # print(human_size(1024 * 1099 * 1024))
    read_text_file()

    pass
