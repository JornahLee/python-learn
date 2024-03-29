import re


# 搜索匹配， 推荐使用 finditer
def find_all():
    # 注意匹配模式！ 默认单行匹配， 可指定多行； 默认大小写敏感
    # re.MULTILINE
    # re.IGNORECASE

    # findall形式，如果存在 子分组，则返回的是所有 子分组的匹配内容， 此处的叠词就不行了
    for i in re.findall(r'(\w)\1(\w)\2', '12 aabb B3123'):
        print(i)
    for i in re.findall(r'((\w)\2(\w)\3)', '12 aabb B3123'):
        print(i)
    # 使用finditer， 就比较灵活，可以精准使用任意分组
    print('-----')
    for i in re.finditer(r'(\w)\1(\w)\2', '12 aabb B3123', re.IGNORECASE):
        # Match.group() 其实就是group(0)， 返回主分组匹配结果，即编号为0的分组
        print(i.group())
        # Match.groups() 以元组形式返回， 子分组的匹配结果， 即编号大于0的分组
        print(i.groups())
    for i in re.finditer(r'((\w)\2(\w)\3)', '12 aabb B3123'):
        # Match.group() 其实就是group(0)， 返回主分组匹配结果，即编号为0的分组
        print(i.group())
        # Match.groups() 以元组形式返回， 子分组的匹配结果， 即编号大于0的分组
        print(i.groups())
    print('-----')

    pass


def replace():
    print('-----------replace-------------\n')
    # python中引用分组使用 \g<1> 方式去引用对应编号的分组.
    # 需要编辑器的分组引用是使用 $1 方式
    res = re.sub(r'(\w)\1(\w)\2', r'66\g<1>66', '1122 woshi aabb')
    print(res)
    # 返回替换了多少处
    res1 = re.subn(r'(\w)\1(\w)\2', '6666', '1122 woshi aabb')
    print(res1)


if __name__ == '__main__':
    # re.compile(r'sdfsd').findall()
    find_all()
    replace()
    # help(re.Match)
    pass
