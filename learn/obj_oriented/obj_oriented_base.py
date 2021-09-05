#!/usr/bin/python
# -*- coding: UTF-8 -*-


# python中也像java 有一个老母亲 object，所有类的父类？ 通过Employee.__bases__查看
class Employee:
    """所有员工的基类"""  # 类的帮助信息可以通过ClassName.__doc__查看。
    empCount = 0  # 类变量，所有实例共享

    # 构造函数__init__()
    # self 代表类的实例，self 在定义类的方法时是必须有的，虽然在调用时不必传入相应的参数
    # self 不是 python 关键字，我们把他换成 其他名字 也是可以正常执行，如 my_self
    # 推测出参数表第一个参数代表实例的引用，与引用名字无关
    # 这个就像java反编译实例方法时：参数表第一个会总是存在一个实例引用一样
    # 构造函数可以重载吗？ python支持重载吗
    # def __init__(my_self, salary):
    #     my_self.salary = salary
    #     Employee.empCount += 1

    # self代表类的实例，而非类
    # 类的方法与普通的函数只有一个特别的区别——它们必须有一个额外的第一个参数名称, 按照惯例它的名称是 self。
    def __init__(self, name, salary):
        # 实例变量
        self.name = name
        self.salary = salary
        Employee.empCount += 1

    # 析构函数 __del__ ，__del__在对象销毁的时候被调用，当对象不再被使用时，__del__方法运行：
    def __del__(self):
        print("enter __del__")
        if hasattr(self, "name"):
            del self.name
        if hasattr(self, "salary"):
            del self.salary
        print("exit __del__")
        pass

    # 等同于java的toString方法
    def __str__(self):
        return "this is __str__ function"

    def display_count(self):
        print("Total Employee %d" % Employee.empCount)

    def display_employee(self):
        print("Name : ", self.name, ", Salary: ", self.salary)

    def show_internal_attr(self):
        print("Employee.__doc__:", Employee.__doc__)
        print("Employee.__name__:", Employee.__name__)
        print("Employee.__module__:", Employee.__module__)
        print("Employee.__bases__:", Employee.__bases__)
        # __dict__ 为类所有属性/字段的 字典
        print("Employee.__dict__:", Employee.__dict__)
        print("Name : ", self.name, ", Salary: ", self.salary)

    def prt(self):
        print(self)
        print(self.__class__)


if __name__ == '__main__':
    # "创建 Employee 类的第一个对象"
    emp1 = Employee("Zara", 2000)
    # "创建 Employee 类的第二个对象"
    emp2 = Employee("Manni", 5000)
    emp1.display_employee()
    emp2.display_employee()
    print("Total Employee %d" % Employee.empCount)
    emp1.show_internal_attr()
    emp1.prt()
    print("------")
    print(hasattr(emp1, 'salary'))  # 如果存在 'age' 属性返回 True。
    print(getattr(emp1, 'salary'))  # 返回 'age' 属性的值
    print(setattr(emp1, 'salary', 8))  # 添加属性 'age' 值为 8
    print(getattr(emp1, 'salary'))  # 返回 'age' 属性的值
    print(delattr(emp1, 'salary'))  # 删除属性 'age'
    print("---emp1---")
    print(emp1.__dict__)
    print("__repr__")
    print(emp1.__repr__())
    print("__repr__")

# python对象销毁(垃圾回收) 一个引用计数器和一个循环垃圾收集器, del 关键字会减少对象的引用
