# 加了星号 * 的参数会以元组(tuple)的形式导入，存放所有未命名的变量参数。
def fun1(age, *args):
    print(age)
    print(args)
    return


# 加了两个星号 ** 的参数会以字典的形式导入。
def fun_dic(age, **args):
    print(age)
    print(args)
    return


# age:int（冒号+类型，用于参数类型提示）， -> str（给函数添加元数据，描述返回值类型，便于开发使用）
def fun2(age: int, name='lic') -> str:
    print(age)
    print(name)
    return str(age) + name


if __name__ == '__main__':
    # 不定长参数 参数前加 *
    fun1(1, 2, "str", 4)
    # 关键词传参，可乱序传参
    fun2(name="123", age=19)
    # 默认参数
    fun2(age=19)
    # **args 代表传入的是字典
    fun_dic(0, a=2, b=3, c=4)
    fun_dic(0)
    # lambda
    sum1 = lambda a, b: print(a + b)
    sum1("sfsdf", "123123")
