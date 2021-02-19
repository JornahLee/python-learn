import threading
# import time
import cv2
from moviepy.editor import *


def tracker_callback(pos):
    global thread
    thread.pos = pos
    pass


# 创建回调函数
def draw_circle(event, x, y, flags, param):
    global ix, iy, drawing, thread
    # 当按下左键时返回起始位置坐标
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    # 当左键按下并移动时绘制图形，event可以查看移动，flag查看是否按下
    elif event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
        if drawing is True:
            cv2.rectangle(param, (ix, iy), (x, y), (0, 255, 0), -1)
    # 当鼠标松开时停止绘图
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        print((ix, iy), (x, y))
        if ix == x and iy == y:
            return
        for index, frame in enumerate(thread.all_frames):
            frame = frame[iy:y, ix:x]
            thread.all_frames[index] = frame

    if param is not None:
        cv2.imshow('video', param)


def btn_callback():
    print('btn_callback')


def play_video(file_name: str):
    global is_Pause, thread
    is_Pause = False
    cap = cv2.VideoCapture(file_name)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    duration = frames / fps
    print(height, width)
    print(fps, frames, duration)

    ret, img = cap.read()
    all_frames = []
    while img is not None:
        all_frames.append(img)
        ret, img = cap.read()
    thread = MyThread('showThread', 0, all_frames, fps)
    thread.start()
    thread.join()


# 子线程自动刷新画面
class MyThread(threading.Thread):
    def __init__(self, name, pos, all_frames, fps=25):
        threading.Thread.__init__(self)
        self.name = name
        self.pos = pos
        self.all_frames = all_frames
        self.fps = fps

    def run(self):
        cv2.namedWindow('video', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
        cv2.createTrackbar('time', 'video', 0, len(self.all_frames), tracker_callback)
        global is_Pause
        print("开始线程：" + self.name)
        while 1:
            cv2.setMouseCallback('video', draw_circle, param=self.all_frames[self.pos])
            cv2.imshow('video', self.all_frames[self.pos])
            input_key = cv2.waitKey(int(1000 / self.fps)) & 0xFF
            if input_key == ord(' '):
                is_Pause = not is_Pause
            elif input_key == ord('q'):
                break
            elif input_key == ord('s'):
                print('time point', int(self.pos / self.fps))
            if not is_Pause:
                self.pos += 1
                cv2.setTrackbarPos('time', 'video', self.pos)
            if self.pos >= len(self.all_frames):
                self.pos = 0
                cv2.setTrackbarPos('time', 'video', self.pos)
            # if 0xFF == ord('q'):
            #     break
        print("退出线程：" + self.name)


def to_gif(file_name: str, speed: float, fps: int, duration: (), rect: (), out: str):
    clip = VideoFileClip(file_name)
    all_param = rect[0] + rect[1]
    out_clip = (clip.set_fps(fps)
                .subclip(*duration)
                .crop(*all_param)
                .fx(vfx.speedx, speed))
    out_clip.write_gif(out)


if __name__ == '__main__':
    global is_Pause, thread
    global ix, iy, drawing
    file = 'D:/SoftwareCache/QQ/614042560/Video/1042E80C04AD79ED596B06B7E1894556.mp4'
    if 1:
        # else分支 获取相关视频剪辑信息
        out_gif = '123' + '.gif'
        re = ((220, 432), (522, 831))
        du = (4, 5.5)
        to_gif(file, speed=0.7, fps=10, duration=du, rect=re, out=out_gif)
    else:
        # s保存时间点,q退出,鼠标左键画出图形区域
        play_video(file)

# 涉及相关知识点
# *args , **args
# 线程休眠 , import time, time.sleep(1.1),unit:second
# python 函数参数可为函数
# (cv2.waitKey(25) & 0xFF) == ord('a')
# 多线程
# open-cv，播放视频使用：逐帧播放
# 暂停视频播放逻辑，做过的错误尝试：
# 1.外层while 1循环，不可以中止，因为还要恢复播放
# 2.暂时采用线程休眠办法，不行，这样需要另一个线程去唤醒，唤醒前啥都做不了
# 3.正确的逻辑为，一直播放当前帧即可。
# 4.举一反三，如果暂停一个循环while index>=0 index++。 直接让index 无法自增即可， 使用线程共享的flag，在另一个线程对flag进行修改即可，但是会涉及到线程安全问题

# 在函数内部，使用global关键字，声明使用外部全局变量，而不是局部变量
