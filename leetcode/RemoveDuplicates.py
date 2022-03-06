def solution(arr: list):
    # arr.forearch
    for index, val in enumerate(arr):
        for index2, val2 in enumerate(arr):
            if val == val2:
                arr.pop(index)
            pass
    pass


if __name__ == '__main__':
    myarr=[1, 2, 34, 2, 3, 2, 3, 3]
    solution(myarr)
    print(myarr)
    pass
