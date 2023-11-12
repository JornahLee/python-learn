import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


def show(*v, **kv) -> None:
    print('\n' + "<< show")
    for i in range(100):
        print('\n' + str(i))
    print('\n' + ">> show")
    time.sleep(1)


if __name__ == '__main__':
    pool = ThreadPoolExecutor(20)
    pool.submit(show, 1, p=1)
    future = pool.submit(lambda a: print(a), 100)
    pool.submit()
    wait([future], return_when=ALL_COMPLETED)
    print('?')
    print(future.result())
