import random
import time
from datetime import datetime
import threading
import random
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED


# python 版本的countdownlatch
# 用于线程同时启动，或多个线程互相等待结束后，再向后执行
class CountDownLatch(object):
    def __init__(self, count=1):
        self.count = count
        self.lock = threading.Condition()

    def count_down(self):
        self.lock.acquire()
        self.count -= 1
        if self.count <= 0:
            self.lock.notifyAll()
        self.lock.release()

    def aawait(self):
        self.lock.acquire()
        while self.count > 0:
            self.lock.wait()
        self.lock.release()


def go_if_ready(signal: CountDownLatch):
    n = random.randint(1, 2)
    time.sleep(n)
    signal.aawait()
    print('\ngo' + datetime.now().__str__())
    pass


def test_start_at_moment():
    count_down_latch = CountDownLatch()
    pool = ThreadPoolExecutor(20)
    for i in range(20):
        pool.submit(go_if_ready, count_down_latch)
    time.sleep(3)
    count_down_latch.count_down()
    pool.shutdown()
    pass


def go_and_say_ready(signal: CountDownLatch):
    time.sleep(3)
    signal.count_down()
    print(threading.currentThread().name + ': done\n')
    pass


def test_start_when_all_ready():
    count_down_latch = CountDownLatch(20)
    pool = ThreadPoolExecutor(20)
    for i in range(20):
        pool.submit(go_and_say_ready, count_down_latch)
    # 等待所有线程count_down完成
    print('waiting for going')
    # count=0时，启动
    count_down_latch.aawait()
    print('go!')
    pass


if __name__ == '__main__':
    test_start_when_all_ready()
    # test_start_at_moment()
