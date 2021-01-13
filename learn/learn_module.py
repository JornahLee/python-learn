from math import sqrt
from math import pi
# import math
import _osx_support


# 同一个module，无论引用多少次，也只有一次有效

# 当解释器遇到 import 语句，如果模块在当前的搜索路径就会被导入。
# 搜索路径是一个解释器会先进行搜索的所有目录的列表。如想要导入模块 support.py，需要把命令放在脚本的顶端：

# 使用模块的方式模块名.函数名


# 模块的搜索路径
# 当你导入一个模块，Python 解析器对模块位置的搜索顺序是：
# 1、当前目录
# 2、如果不在当前目录，Python 则搜索在 shell 变量 PYTHONPATH 下的每个目录。
# 3、如果都找不到，Python会察看默认路径。UNIX下，默认路径一般为/usr/local/lib/python/。
# 模块搜索路径存储在 system 模块的 sys.path 变量中。变量里包含当前目录，PYTHONPATH和由安装过程决定的默认目录。

if __name__ == '__main__':
    print(dir(_osx_support))
    print(sqrt(4))
    print(bin(100))
    print(pi)

# 变量作用域
# 在局部作用域声明全局变量：函数内的全局变量赋值，必须使用 global 语句。



# Python中定义包
# 包是一个分层次的文件目录结构，它定义了一个由模块及子包，和子包下的子包等组成的 Python 的应用环境。
# 简单来说，包就是文件夹，但该文件夹下必须存在 __init__.py 文件, 该文件的内容可以为空。__init__.py 用于标识当前文件夹是一个包。
# 考虑一个在 package_runoob 目录下的 runoob1.py、runoob2.py、__init__.py 文件，test.py 为测试调用包的代码，目录结构如下：
# test.py
# package_runoob
# |-- __init__.py
# |-- runoob1.py
# |-- runoob2.py