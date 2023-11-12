# UTF-8
# author hestyle
# desc: 必须在终端直接执行，不能在pycharm等IDE中直接执行，否则看不到动态进度条效果
# author jornah， enhance,小优化，下载失败后，重新下载会跳过已下载文件

import os
import sys
import m3u8
import requests
import traceback
import threadpool
from Crypto.Cipher import AES

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
}
# 代理设置
proxies = {
    # export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

######################配置信息##########################
# m3u8链接批量输入文件
m3u8InputFilePath = "./m3u8s_input.txt"
# 视频保存路径
# m3u8文件、key文件下载尝试次数，ts流默认无限次尝试下载，直到成功
m3u8TryCountConf = 10
# 线程数（同时下载的分片数）
processCountConf = 50
#######################################################

# 全局变量
# 全局线程池
taskThreadPool = threadpool.ThreadPool(processCountConf)
# 当前下载的m3u8 url
# ts count
sumCount = None
# 已处理的ts
doneCount = None
# cache path
# log path
logFile = open('./log', "w+", encoding="utf-8")


def log(msg: str):
    print(msg)
    logFile.write(f'\n{msg}')


# 1、下载m3u8文件
def getM3u8Info(m3u8Url):
    tryCount = m3u8TryCountConf
    while True:
        if tryCount < 0:
            log("\t{0}下载失败！".format(m3u8Url))
            log("\t{0}下载失败！".format(m3u8Url))
            return None
        tryCount = tryCount - 1
        try:
            response = requests.get(m3u8Url, headers=headers, timeout=20, allow_redirects=True, proxies=proxies)
            if response.status_code == 301:
                nowM3u8Url = response.headers["location"]
                log("\t{0}重定向至{1}！".format(m3u8Url, nowM3u8Url))
                log("\t{0}重定向至{1}！\n".format(m3u8Url, nowM3u8Url))
                m3u8Url = nowM3u8Url
                continue
            expected_length = int(
                '0' if response.headers.get('Content-Length') is None else response.headers.get('Content-Length'))
            actual_length = len(response.content)
            if expected_length > actual_length:
                # raise Exception("m3u8下载不完整")
                log('warning!!!  m3nu 可能下载不完成.....')

            log("\t{0}下载成功！".format(m3u8Url))
            log("\t{0}下载成功！".format(m3u8Url))
            rootUrlPath = m3u8Url[0:m3u8Url.rindex('/')]
            break
        except TimeoutError:
            log("\t{0}下载失败！正在重试".format(m3u8Url))
            log("\t{0}下载失败！正在重试".format(m3u8Url))
            traceback.print_exc()
    # 解析m3u8中的内容
    m3u8Info = m3u8.loads(response.text)
    # 有可能m3u8Url是一个多级码流
    if m3u8Info.is_variant:
        log("\t{0}为多级码流！".format(m3u8Url))
        log("\t{0}为多级码流！".format(m3u8Url))
        for rowData in response.text.split('\n'):
            # 寻找响应内容的中的m3u8
            if rowData.endswith(".m3u8"):
                subM3u8Url = m3u8Url.replace("index.m3u8", rowData)
                rootUrlPath = m3u8Url[0:m3u8Url.rindex('/')]
                return getM3u8Info(subM3u8Url)
        # 遍历未找到就返回None
        log("\t{0}响应未寻找到m3u8！".format(response.text))
        log("\t{0}响应未寻找到m3u8！".format(response.text))
        return None
    else:
        return m3u8Info, rootUrlPath


# 2、下载key文件
def getKey(keyUrl):
    tryCount = m3u8TryCountConf
    while True:
        if tryCount < 0:
            log("\t{0}下载失败！".format(keyUrl))
            log("\t{0}下载失败！".format(keyUrl))
            return None
        tryCount = tryCount - 1
        try:
            response = requests.get(keyUrl, headers=headers, timeout=20, allow_redirects=True, proxies=proxies)
            if response.status_code == 301:
                nowKeyUrl = response.headers["location"]
                log("\t{0}重定向至{1}！".format(keyUrl, nowKeyUrl))
                log("\t{0}重定向至{1}！\n".format(keyUrl, nowKeyUrl))
                keyUrl = nowKeyUrl
                continue
            expected_length = int(response.headers.get('Content-Length'))
            actual_length = len(response.content)
            if expected_length > actual_length:
                raise Exception("key下载不完整")
            log("\t{0}下载成功！key = {1}".format(keyUrl, response.content.decode("utf-8")))
            log("\t{0}下载成功！ key = {1}".format(keyUrl, response.content.decode("utf-8")))
            break
        except:
            log("\t{0}下载失败！".format(keyUrl))
            log("\t{0}下载失败！".format(keyUrl))
    return response.text


# 3、多线程下载ts流
def mutliDownloadTs(playlist, workPath):
    global sumCount
    global doneCount
    taskList = []
    # 每个ts单独作为一个task
    for index in range(len(playlist)):
        dict = {"playlist": playlist, "index": index, "workPath": workPath}
        taskList.append((None, dict))
    # 重新设置ts数量，已下载的ts数量
    doneCount = 0
    sumCount = len(taskList)
    printProcessBar(sumCount, doneCount, 50)
    # 构造thread pool
    requests = threadpool.makeRequests(downloadTs, taskList)
    [taskThreadPool.putRequest(req) for req in requests]
    # 等待所有任务处理完成
    taskThreadPool.wait()
    print("")
    return True


def createCurrentDir(pathname: str):
    # pathname

    dirname = os.path.dirname(pathname)
    if not os.path.exists(dirname):
        if os.path.isdir(pathname):
            os.makedirs(pathname)
        else:
            os.makedirs(dirname)


# 4、下载单个ts playlists[index]
def downloadTs(playlist, index, workPath):
    global sumCount
    global doneCount
    succeed = False
    outputPath = f'{workPath}/{index:0>8}.ts'
    createCurrentDir(outputPath)
    ts_is_exists = os.path.exists(outputPath)

    tsUrl = playlist[index]
    while not succeed and not ts_is_exists:
        # 文件名格式为 "00000001.ts"，index不足8位补充0
        outputFp = open(outputPath, "wb+")
        if not playlist[index].startswith("http"):
            log('error invalid ts url')
        try:
            log("\t分片{0:0>8} url = {1} 下载ing....！".format(index, tsUrl))
            response = requests.get(tsUrl, timeout=10, headers=headers, stream=True, proxies=proxies)
            if response.status_code == 200:
                expected_length = int(response.headers.get('Content-Length'))
                actual_length = len(response.content)
                if expected_length > actual_length:
                    raise Exception("分片下载不完整")
                outputFp.write(response.content)
                succeed = True
                log("\t分片{0:0>8} url = {1} 下载成功！".format(index, tsUrl))
        except Exception as exception:
            log("\t分片{0:0>8} url = {1} 下载失败！正在重试...msg = {2}".format(index, tsUrl, exception))
        outputFp.close()
    if succeed or ts_is_exists:
        doneCount += 1
        printProcessBar(sumCount, doneCount, 50)


# 5、合并ts
def mergeTs(tsFileDir, outputFilePath, cryptor, count):
    createCurrentDir(outputFilePath)
    outputFp = open(outputFilePath, "wb+")
    for index in range(count):
        printProcessBar(count, index + 1, 50)
        log("\t{0}\n".format(index))
        inputFilePath = tsFileDir + "/" + "{0:0>8}.ts".format(index)
        if not os.path.exists(outputFilePath):
            log("\n分片{0:0>8}.ts, 不存在，已跳过！".format(index))
            log("分片{0:0>8}.ts, 不存在，已跳过！\n".format(index))
            continue
        inputFp = open(inputFilePath, "rb")
        fileData = inputFp.read()
        try:
            if cryptor is None:
                outputFp.write(fileData)
            else:
                outputFp.write(cryptor.decrypt(fileData))
        except Exception as exception:
            inputFp.close()
            outputFp.close()
            print(exception)
            return False
        inputFp.close()
    print("")
    outputFp.close()
    return True


# 6、删除ts文件
def removeTsDir(tsFileDir):
    log(f'清空cache 文件夹{tsFileDir} ....')
    # 先清空文件夹
    for root, dirs, files in os.walk(tsFileDir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(tsFileDir)
    return True


# 7、convert to mp4（调用了FFmpeg，将合并好的视频内容放置到一个mp4容器中）
def ffmpegConvertToMp4(inputFilePath, ouputFilePath):
    if not os.path.exists(inputFilePath):
        log(inputFilePath + " 路径不存在！")
        log(inputFilePath + " 路径不存在！\n")
        return False
    cmd = r'ffmpeg -i "{0}" -vcodec copy -acodec copy "{1}"'.format(inputFilePath, ouputFilePath)
    if os.system(cmd) == 0:
        log(inputFilePath + "转换成功！")
        log(inputFilePath + "转换成功！\n")
        return True
    else:
        log(inputFilePath + "转换失败！")
        log(inputFilePath + "转换失败！\n")
        return False


# 8、模拟输出进度条
def printProcessBar(sumCount, doneCount, width):
    precent = doneCount / sumCount
    useCount = int(precent * width)
    spaceCount = int(width - useCount)
    precent = precent * 100
    print('\t{0}/{1} {2}{3} {4:.2f}%'.format(sumCount, doneCount, useCount * '■', spaceCount * '□', precent),
          file=sys.stdout, flush=True, end='\r')


# m3u8下载器
def processDownloadM3u8(title, m3u8Url, workPath):
    videoPath = f'{workPath}/{title}.mp4'
    if os.path.exists(videoPath):
        log(f'{videoPath} 已下载完毕')
        return True

    createCurrentDir(workPath)
    # 1、下载m3u8
    log("\t1、开始下载m3u8...")
    log("\t1、开始下载m3u8...\n")
    m3u8Info, rootUrlPath = getM3u8Info(m3u8Url)
    if m3u8Info is None:
        return False
    tsList = []
    for playlist in m3u8Info.segments:
        tsName = str(playlist.uri)
        tsUrl = tsName if tsName.startswith('http') else f'{rootUrlPath}/{tsName}'
        tsList.append(tsUrl)
    cryptor = getCrypor(m3u8Info, m3u8Url)
    # 3、下载ts
    log("\t3、开始下载ts...")
    tsTempPath = f"{workPath}/cache"
    if mutliDownloadTs(tsList, tsTempPath):
        log("\tts下载完成---------------------\n")
    mergedFilePath = f"{tsTempPath}/cache.flv"
    mergeTsFiles(cryptor, tsList, tsTempPath, mergedFilePath)
    log("\t5、开始mp4转换...\n")
    if not ffmpegConvertToMp4(mergedFilePath, videoPath):
        return False
    if os.path.exists(videoPath):
        removeTsDir(tsTempPath)
    return True


def mergeTsFiles(cryptor, tsList, workPath, mergedFilePath):
    log("\t4、开始合并ts...")
    log("\t4、开始合并ts...\n")
    if mergeTs(workPath, mergedFilePath, cryptor, len(tsList)):
        log("\tts合并完成---------------------")
        log("\tts合并完成---------------------\n")
    else:
        log("\tts合并失败！")
        log("\tts合并失败！\n")


def getCrypor(m3u8Info, m3u8Url):
    # 2、获取key
    cryptor = None
    # 判断是否加密
    if (len(m3u8Info.keys) != 0) and (m3u8Info.keys[0] is not None):
        # 默认选择第一个key，且AES-128算法
        key = m3u8Info.keys[0]
        if key.method != "AES-128":
            log("\t{0}不支持的解密方式！".format(key.method))
            log("\t{0}不支持的解密方式！\n".format(key.method))
            return cryptor
        # 如果key的url是相对路径，加上m3u8Url的路径
        keyUrl = key.uri
        if not keyUrl.startswith("http"):
            keyUrl = m3u8Url.replace("index.m3u8", keyUrl)
        log("\t2、开始下载key...")
        log("\t2、开始下载key...\n")
        keyText = getKey(keyUrl)
        if keyText is None:
            return cryptor
        # 判断是否有偏移量
        if key.iv is not None:
            cryptor = AES.new(bytes(keyText, encoding='utf8'), AES.MODE_CBC, bytes(key.iv, encoding='utf8'))
        else:
            cryptor = AES.new(bytes(keyText, encoding='utf8'), AES.MODE_CBC, bytes(keyText, encoding='utf8'))
    return cryptor


def main():
    if not (os.path.exists(m3u8InputFilePath)):
        log("{0}文件不存在！".format(m3u8InputFilePath))
        with open(m3u8InputFilePath, 'w') as f:
            f.write('title,m3u8_url')
            log('自动创建M3U8输入文件，请输入文件 title,m3u8_url')
            pass
        exit(0)

    with open(m3u8InputFilePath, "r", encoding="utf-8") as m3u8InputFp:
        while True:
            rowData = m3u8InputFp.readline()
            rowData = rowData.strip('\n')
            if rowData == "":
                break
            m3u8Info = rowData.split(',')
            title = m3u8Info[0]
            m3u8Url = m3u8Info[1]
            try:
                log("{0} 开始下载:".format(m3u8Info[0]))
                log("{0} 开始下载:\n".format(m3u8Info[0]))
                if processDownloadM3u8(title, m3u8Url, f'./output/{title}'):
                    log("{0} 下载成功！".format(m3u8Info[0]))
                else:
                    log("{0} 下载失败！".format(m3u8Info[0]))
                    log("{0} 下载失败！\n".format(m3u8Info[0]))
            except Exception as exception:
                print(exception)
                traceback.print_exc()
    # 关闭文件
    log("----------------下载结束------------------")


def downloadM3u8(download_list: [[]]):
    for item in download_list:
        title = item[0]
        m3u8Url = item[1]
        processDownloadM3u8(title, m3u8Url, f'./output/{title}')
    pass


if __name__ == '__main__':
    # 判断m3u8文件是否存在
    downloadM3u8([['nice','https://t23a.cdn2020.com/video/m3u8/2023/11/10/cea5f674/index.m3u8']])
    # main()
