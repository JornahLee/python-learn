#!/usr/bin/python
# -*- coding: UTF-8 -*-


def success():
    try:
        fh = open("testfile", "r")
        fh.write("这是一个测试文件，用于测试异常!!")
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    else:
        print("内容写入文件成功")
        fh.close()


def exception():
    try:
        fh = open("testfile", "w")
        fh.write("这是一个测试文件，用于测试异常!!")
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    else:
        print("内容写入文件成功")
        fh.close()


def final():
    try:
        fh = open("testfile", "r")
        fh.write("这是一个测试文件，用于测试异常!!")
    except IOError:
        print("Error: 没有找到文件或读取文件失败")
    else:
        print("内容写入文件成功")
        fh.close()
    finally:
        print("this is finally")


def with_args():
    try:
        return int('var')
    except ValueError as Argument:
        print(ValueError)
        print("参数没有包含数字\n", Argument)


def raise_exc():
    raise ValueError('123', "trace")


if __name__ == '__main__':
    # 没有异常，则进入else分支，类似于for else，没有跳出循环则执行else分支
    # try不可单独出现，try finally， try except, try except finally
    # 可嵌套
    # success()
    # exception()
    # final()
    # with_args()
    try:
        raise_exc()
    except ValueError as Argument:
        print(ValueError)
        print(Argument)
        print(type(Argument))

# 用户自定义异常
# 通过创建一个新的异常类，程序可以命名它们自己的异常。异常应该是典型的继承自Exception类，通过直接或间接的方式。
# 以下为与RuntimeError相关的实例,实例中创建了一个类，基类为RuntimeError，用于在异常触发时输出更多的信息。
# 在try语句块中，用户自定义的异常后执行except块语句，变量 e 是用于创建Networkerror类的实例。
# class Networkerror(RuntimeError):
#     def __init__(self, arg):
#         self.args = arg
