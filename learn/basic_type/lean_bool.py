# Python逻辑运算符：  and  or  not (非0（非空）则为真,)  ， python 并不支持 switch 语句
def test_logic_calc():
    a = [1, 2]
    b = 2
    # and or 还是老老实实用在bool值之间吧, 感觉用or来实现if else效果容易混淆，且不便于理解
    print(a or b)  # [1, 2]
    print(True or 100)  # True,  a or b 相当于 if a==true return true. else return b
    print(False or 100)  # 100
    print(True and 100)  # 100, a and b 相当于 if a==true return b. else return False
    print(False and 100)  # False
    print(1 or 2)  # 1
    print(1 and 2)  # 2
    print('---')


if __name__ == '__main__':
    test_logic_calc()
    pass
