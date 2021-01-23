import re
from urllib.request import urlopen

# Python3字符串前缀u、b、r
# u前缀：字符串默认创建即以Unicode编码存储，可以存储中文。
# r前缀：主要解决的是 转义字符，特殊字符 的问题，其中所有字符均视为普通字符。
# b前缀：字符串存储为Ascll码，无法存储中文。
if __name__ == '__main__':
    print(re.findall(r'\bf[a-z]*', 'which foot or hand fell fastest'))
    a = r'asd'
    print(a)
    resp = urlopen('https://www.baidu.com')
    print(type(resp))
    print(resp.__dict__)
    for line in resp:
        line = line.decode('utf-8')  # Decoding the binary data to text.
        print(line)
