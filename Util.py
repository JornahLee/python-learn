

# 存储容量 易读
def human_size(byte_size: int):
    kb = byte_size / 1024
    if kb < 1000:
        return '%.2f' % kb + ' kb'
    mb = kb / 1024
    if mb < 1000:
        return '%.2f' % mb + ' mb'
    gb = mb / 1024
    if gb < 1000:
        return '%.2f' % gb + ' gb'
