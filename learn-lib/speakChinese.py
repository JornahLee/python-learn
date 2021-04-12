# coding:utf-8

import pyttsx3

# 依赖安装
# pip install pyttsx3
# 若未安装pywin32, 需要安装此库的 pip install pywin32

if __name__ == '__main__':

    # 初始化
    engine = pyttsx3.init()

    voices = engine.getProperty('voices')
    # 语速控制
    rate = engine.getProperty('rate')
    print(rate)
    engine.setProperty('rate', rate)

    # 音量控制
    volume = engine.getProperty('volume')
    print(volume)
    engine.setProperty('volume', volume)

    # engine.say('hello world')
    while True:
        text = input()
        engine.say(text)
        engine.runAndWait()
    # 朗读一次
    # engine.runAndWait()
    #
    # engine.say('语音合成开始')
    # engine.say('我会说中文了，开森，开森')
    # engine.runAndWait()
    #
    # engine.say('The quick brown fox jumped over the lazy dog.')
    # engine.runAndWait()
    #
    # # 更换语种--zh_HK
    # engine.setProperty('voice', "com.apple.speech.synthesis.voice.sin-ji")
    # engine.setProperty('voice', "VoiceGenderMale")
    # engine.say('从方法声明上来看，第一个参数指定的是语音驱动的名称，这个在底层适合操作系统密切相关的。')
    #
    # # 更换语种--zh_CN
    # engine.setProperty('voice', "com.apple.speech.synthesis.voice.ting-ting.premium")
    # engine.say('从方法声明上来看，第一个参数指定的是语音驱动的名称，这个在底层适合操作系统密切相关的。')
    #
    # # 更换语种--zh_TW
    # engine.setProperty('voice', "com.apple.speech.synthesis.voice.mei-jia")
    # engine.say('从方法声明上来看，第一个参数指定的是语音驱动的名称，这个在底层适合操作系统密切相关的。')
    # engine.runAndWait()
    # print(engine.getProperty("voices"))
    #
    # for voice in voices:
    #     print(voice)
    #     engine.setProperty("voice", voice.id)
