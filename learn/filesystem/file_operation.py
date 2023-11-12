#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os


def createCurrentDir(pathname: str):
    # pathname
    dirname = os.path.dirname(pathname)
    if not os.path.exists(dirname):
        if os.path.isdir(pathname):
            os.makedirs(pathname)
        else:
            os.makedirs(dirname)


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
    temp = []
    recurse_path("/Users/macbook/logs", lambda x: temp.append(x), max_depth=1)
    print(temp)


# 递归遍历path
def test_walk():
    path = "/Users/macbook/logs"
    # return 元组(dir_path, dir_names, filenames)
    for i in os.walk(path):
        for item in i[2]:
            ab_file_path = os.path.join(path, item)
            print(ab_file_path)


if __name__ == '__main__':
    createCurrentDir('./test/test/2123/')
    # 测试递归遍历
    # test_path_recurse()
    # test_walk()
    # file_operation()
    # read_text_file()

    pass
