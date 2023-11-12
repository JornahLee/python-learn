# 文件 大小 存储容量 易读
def human_size(byte_size: int):
    kb = byte_size / 1024
    if kb < 1000:
        # 保留小数点后两位， %号的使用
        return '%.2f' % kb + ' kb'
    mb = kb / 1024
    if mb < 1000:
        return '%.2f' % mb + ' mb'
    gb = mb / 1024
    if gb < 1000:
        return '%.2f' % gb + ' gb'
    tb = gb / 1024
    return '%.2f' % tb + ' tb'


if __name__ == '__main__':
    print(human_size(2306397437952))
