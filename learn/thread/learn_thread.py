from threading import Thread
import time


class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        show()


def show():
    print('\n' + "<< show")
    for i in range(100):
        print('\n' + str(i))
    print('\n' + ">> show")
    time.sleep(10)


if __name__ == '__main__':
    t1 = Thread(target=show)
    t2 = MyThread()
    t1.start()
    t2.start()
    t1.join()  # 当前线程等待t1线程结束后，再向下执行
    print('----t1执行完毕----')
    t2.join()
