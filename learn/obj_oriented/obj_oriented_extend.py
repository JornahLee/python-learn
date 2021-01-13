#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ParentClass:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        # 定义私有实例变量
        self.__length = 1
        pass

    def show(self):
        print("parent show")

    def __pri_show(self):
        print(str(self.__length) + "private show")


# class 派生类名(基类名)
class SubClass(ParentClass):
    def __init__(self, name, age, clothes):
        # 调用父类实例方法时，需要带上子类的实例引用
        ParentClass.__init__(self, name, age)
        self.clothes = clothes
        pass

    def show(self):
        ParentClass.show(self)
        print("sub show")



if __name__ == '__main__':
    sub = SubClass("lic", 14, "jacket")
    print(issubclass(SubClass, ParentClass))
    print(isinstance(sub, SubClass))
    print(isinstance(sub, ParentClass))
    print(sub.__dict__)
    print("---------")
    # SubClass.__cmp__(1,2)
    # print(sub.__length) # 无法在类外访问私有变量
    # print(sub.__pri_show) # 无法在类外访问私有方法
    sub.show()
    # sub.__class___name
    # Python不允许实例化的类访问私有数据，但你可以使用 object._className__attrName（ 对象名._类名__私有属性名 ）访问属性，参考以下实例：

