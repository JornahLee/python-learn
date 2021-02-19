from threading import Thread, Lock, enumerate
import time

num = 0
mutex = Lock()


def add_num():
    global num
    for i in range(100000):
        mutex.acquire()
        num += 1
        mutex.release()


if __name__ == '__main__':
    t1 = Thread(target=add_num)
    t2 = Thread(target=add_num)
    t3 = Thread(target=add_num)
    t1.start()
    t2.start()
    t3.start()

    while len(enumerate()) != 1:
        time.sleep(1)
