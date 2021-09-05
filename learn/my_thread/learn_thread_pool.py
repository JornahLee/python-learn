import time
from concurrent.futures import ThreadPoolExecutor


def show(*v, **kv) -> None:
    print('\n' + "<< show")
    for i in range(100):
        print('\n' + str(i))
    print('\n' + ">> show")
    time.sleep(10)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(20)
    pool.submit(show, 1, p=1)
    pool.submit(lambda a: print(a), 100)
