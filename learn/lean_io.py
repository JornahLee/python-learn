#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os


def open_file():
    file = open('123.py')
    # print(file.readline(2))
    res = file.read(20)

    print(file.name)
    print(file.tell())
    file.seek
    print(res)
    print(type(res))
    return


def standard_input():
    # 标准输入
    str1 = input("input:")
    # 标准输出
    print(str1)


def file_op():
    os.rename("re_123.py", "123.py")
    os.remove("filename")
    os.mkdir("filename")
    # chdir()
    # rmdir()


if __name__ == '__main__':
    file_op()


