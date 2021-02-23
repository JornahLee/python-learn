#!/usr/bin/python
# -*- coding: UTF-8 -*-

# 生成器
# 在 Python 中，使用了 yield 的函数被称为生成器（generator）。
# 跟普通函数不同的是，生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。
# 在调用生成器运行的过程中，每次遇到 yield 时函数会暂停并保存当前所有的运行信息，返回 yield 的值, 并在下一次执行 next() 方法时从当前位置继续运行。
# 调用一个生成器函数，返回的是一个迭代器对象。
# 以下实例使用 yield 实现斐波那契数列：

# !/usr/bin/python3

import sys


def fibonacci(n):  # 生成器函数 - 斐波那契
    a, b, counter = 0, 1, 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


if __name__ == '__main__':

    f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成

    while True:
        try:
            print(next(f), end=" ")
        except StopIteration:
            sys.exit()

# todo
# 常量
# 日志
# 全局变量
# 正确封装函数


# todo
# 环境安装，安装python
# debian 安装pip3 sudo apt install python3-pip



# python 有python2和python3的区别
# 那么pip也有pip和pip3的区别
# 大概是这样的
# 1、pip是python的包管理工具，pip和pip3版本不同，都位于Scripts\目录下：
# 2、如果系统中只安装了Python2，那么就只能使用pip。
# 3、如果系统中只安装了Python3，那么既可以使用pip也可以使用pip3，二者是等价的。
# 4、如果系统中同时安装了Python2和Python3，则pip默认给Python2用，pip3指定给Python3用。
# 5、重要：虚拟环境中，若只存在一个python版本，可以认为在用系统中pip和pip3命令都是相同的
