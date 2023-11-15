

# Python和java类似，None就是null。 没有js中的undefined, NaN
def main():
    print(None is None)  # True, None 空类型，类似java中的null, 对象声明不赋值就是None
    print(None == None)  # True
    print("" in "sdfsf")
    print(not 0)  # True
    print(not 1)  # False
    print(not '')  # True
    print(not [])  # True
    print(not ' ')  # False
    print(not None)  # True
    # 在Python中，以下值被视为逻辑假（False）：
    # 1. None
    # 2. False
    # 3. 0（整数）
    # 4. 0.0（浮点数）
    # 5. ''（空字符串）
    # 6. []（空列表）
    # 7. ()（空元组）
    # 8. {}（空字典）
    # 9. set()（空集合）
    # 除了上述值外，其他任何非空非零的值都被视为逻辑真（True）。这种逻辑判定在条件语句和布尔运算中经常使用。


if __name__ == '__main__':
    main()
