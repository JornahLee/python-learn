import re

def sqlParamIndex():
    str = """insertinto xxxx(f1,f2,f3,f4,f5)
          values(1,?,?,'!',?)"""
    # 注意sql中的函数包含括号，因此需要手动去除
    res = re.findall(r"\(.+?\)", str, re.MULTILINE)
    field_str = res[0]
    print(field_str)
    value_str = res[1]
    print(value_str)
    field_arr = field_str[1:-1].split(",")
    print(field_arr)
    value_arr = value_str[1:-1].split(",")
    print(value_arr)
    count = 0
    for index, val in enumerate(value_arr):
        if val == '?':
            count += 1
            field_arr[index] = field_arr[index] + ' (%d) ' % count
        pass
    print('-----')
    print('-----')
    print('-----')
    for index, val in enumerate(field_arr):
        print(val, end=',' if index % 5 != 0 else '\n')
    pass


if __name__ == '__main__':
    # count = 1
    # str1 = '1231'
    # print(str1 + '(%d)' % count)
    sqlParamIndex()
    pass
