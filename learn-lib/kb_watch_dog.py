import keyboard
# github addr:https://github.com/boppreh/keyboard
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import re
from threading import Thread


class MsgHolder:
    def __init__(self):
        self.i = 0
        self.li = [
            '你真菜',
            '你技术不行',
            ' 你xx死了'
        ]

    def set_msg(self, msg_list):
        self.li = msg_list

    def get_current_msg(self):
        return self.li[self.i]

    def left(self):
        self.i -= 1
        if self.i >= len(self.li):
            self.i = 0
        if self.i < 0:
            self.i = len(self.li) - 1
        return self.li[self.i]

    def right(self):
        self.i += 1
        if self.i >= len(self.li):
            self.i = 0
        if self.i < 0:
            self.i = len(self.li) - 1
        return self.li[self.i]


class MsgSender:
    def __init__(self, msg_holder: MsgHolder):
        self.press_delay = 0.03
        self.input_delay = 0.03
        self.msg_holder = msg_holder
        self.is_send_all = False
        self.is_on = False

    def ready_input(self):
        time.sleep(self.press_delay)
        if self.is_send_all:
            self.press_and_release('shift+enter')
        else:
            self.press_and_release('enter')

    def send_input(self):
        time.sleep(self.press_delay)
        self.press_and_release('enter')

    def press_and_release(self, k, *dy):
        if len(dy) == 0:
            time.sleep(self.press_delay)
        else:
            time.sleep(*dy)
        keyboard.press_and_release(k)

    def send(self, msg):
        arr = msg.split(' ')
        for m in arr:
            self.ready_input()
            time.sleep(self.input_delay)
            keyboard.write(m)
            self.send_input()

    def switch(self):
        self.is_on = not self.is_on
        if self.is_on:
            print('\n------喷人开启------\n')
            keyboard.add_hotkey('page down', next_msg)
            keyboard.add_hotkey('end', send_msg)
            keyboard.add_hotkey('page up', last_msg)
            keyboard.add_hotkey('del', switch_send_all)
        else:
            print('\n------喷人关闭------\n')
            keyboard.remove_hotkey('page down')
            keyboard.remove_hotkey('end')
            keyboard.remove_hotkey('page up')
            keyboard.remove_hotkey('del')

    def switch_send_all(self):
        self.is_send_all = not self.is_send_all
        if self.is_send_all:
            print('\n------关闭 所有人------\n')
        else:
            print('\n------开启 所有人------\n')


class MyHandler(FileSystemEventHandler):
    def __init__(self, holder: MsgHolder, file_name=''):
        super().__init__()
        self.file_name = file_name
        self.holder = holder

    def load_sentences(self):
        try:
            with open(self.file_name, 'r', encoding="utf-8") as f:
                li = str(f.read()).split('\n')
                f = filter(lambda x: (
                        len(re.sub(r'\s*', '', x)) > 0 and not x.startswith('#')
                ), li)
                self.holder.set_msg(list(f))
        except Exception as ex:
            print(ex)

    def on_any_event(self, event):
        if event.src_path.__contains__(self.file_name):
            self.load_sentences()


def send_msg():
    msg = msg_sender.msg_holder.get_current_msg()
    msg_sender.send(msg)


def last_msg():
    msg = msg_sender.msg_holder.left()
    msg_sender.send(msg)


def next_msg():
    msg = msg_sender.msg_holder.right()
    msg_sender.send(msg)


def switch_send_all():
    msg_sender.switch_send_all()


def switch():
    msg_sender.switch()


def watch_file():
    path = '脏话配置文件.txt'
    event_handler = MyHandler(msg_sender.msg_holder, path)
    event_handler.load_sentences()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=False)
    observer.start()
    observer.join()


msg_sender = MsgSender(MsgHolder())


def lianzhao():
    msg_sender.press_and_release('e')
    msg_sender.press_and_release('w')
    msg_sender.press_and_release('q')
    msg_sender.press_and_release('2')
    time.sleep(0.3)

    msg_sender.press_and_release('e')
    msg_sender.press_and_release('q')
    time.sleep(0.3)
    msg_sender.press_and_release('d')
    msg_sender.press_and_release('e')
    msg_sender.press_and_release('q')
    time.sleep(0.1)
    msg_sender.press_and_release('r')


if __name__ == '__main__':
    tips = """
    一键骂人已启动！！
    务必右键使用管理员运行此软件
     使用方法: 方向键 (page up) (page down) 切换上一句/下一句
     (del)  切换发送所有人
     (home) 关闭骂人
     (end) 再次发送当前句子
     配置骂人的句子在当前文件夹下
     要被屏蔽的词语，要使用空格隔开，不然会被河蟹 比如:  你 妈 死 了
    """
    print(tips)
    t1 = Thread(target=watch_file)
    t1.start()
    keyboard.add_hotkey('home', switch)
    # keyboard.add_hotkey('page down', lianzhao)
    keyboard.wait()
