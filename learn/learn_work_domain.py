# Python3 命名空间和作用域

# 命名空间

# 一般有三种命名空间：
#
# 内置名称（built-in names）， Python 语言内置的名称，比如函数名 abs、char 和异常名称 BaseException、Exception 等等。
# 全局名称（global names），模块中定义的名称，记录了模块的变量，包括函数、类、其它导入的模块、模块级的变量和常量。
# 局部名称（local names），函数中定义的名称，记录了函数的变量，包括函数的参数和局部定义的变量。（类中定义的也是）

# 访问命名，采取就近原则
# 假设我们要使用局部变量 runoob，则 Python 的查找顺序为：局部的命名空间去 -> 全局命名空间 -> 内置命名空间。


# 作用域
# Python 中只有模块（module），类（class）以及函数（def、lambda）才会引入新的作用域，
# 其它的代码块（如 if/elif/else/、try/except、for/while等）是不会引入新的作用域的，也就是说这些语句内定义的变量，外部也可以访问，如下代码：
def test_domain():
    for i in range(1, 10):
        print(i)
    print(i)


# 闭包
# 外部函数A中定义了变量x和内部函数B，倘若内部函数B使用了变量x，就形成了闭包，即B函数成为了闭包
# 如果不用外部函数的变量，则没有形成闭包

if __name__ == '__main__':
    test_domain()
