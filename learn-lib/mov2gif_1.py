from moviepy.editor import *


def maomi():
    clip = (VideoFileClip("/Users/licong/Downloads/maomi.mp4")
            # .subclip(1, 2)
            .set_fps(7)
            # .resize((100, 100))
            .crop(x1=0, width=500, y1=0, height=500)
            .resize(0.3)
            )
    print(clip.size)
    print(clip.size)
    # clip.write_gif(filename="maomi.gif", fuzz=0.01)
    print(clip.__class__.__bases__)


def speed_plus():
    clip = (VideoFileClip("/Users/licong/Downloads/pink.gif")
            .fx(vfx.speedx, 2)
            )
    clip.write_gif(filename="ppp.gif")


if __name__ == '__main__':
    name = "aadas"
    file_format = ".mp4"
    path = "/Users/licong/Downloads/"
    clip = (VideoFileClip(path + name + file_format)
            # .fx(vfx.speedx, 2)
            # .subclip(t_start=10)
            .resize(0.5)
            .set_fps(10)
            )
    print(clip.end)
    output_name = name + ".gif"
    clip.write_gif(filename=output_name, fuzz=0.01)
