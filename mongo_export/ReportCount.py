import re


def count():
    total = 0
    with open('report-data.txt', encoding='utf-8') as f:
    # with open('report-data-error13-37.txt', encoding='utf-8') as f:
        cont = f.read()
        res = re.findall(r'(?<=rowCountFromCode=)\d+', cont)
        for r in res:
            total = total + int(r)
        pass
    print(total)


if __name__ == '__main__':
    # with open('report-id.txt', encoding='utf-8') as f:
    #     cont = f.read()
    #     res = re.findall(r'report:RS.+', cont)
    #     print(res)
    #     print(len(set(res)))
    #     pass

    count()
    pass
