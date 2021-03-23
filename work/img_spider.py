import requests  # pip3 install requests
from bs4 import BeautifulSoup  # pip3 install beautifulsoup4,依赖pip3 install lxml
import re
import time
import os

headers = {
    # 存储任意的请求头信息
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
}


def download_with_link(img_url: str):
    folder_name = 'imgs'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    print("download img", img_url)
    file_suffix = get_file_suffix(img_url)
    try:
        img_resp = requests.get(img_url, headers=headers)
        with open("imgs/" + str(time.time()) + file_suffix, 'wb') as f:
            f.write(img_resp.content)
    except Exception as e:
        print("error", e)


def get_file_suffix(url: str) -> str:
    return re.search(r"\.\w{3,5}$", url).group()


if __name__ == '__main__':
    page_url = 'https://www.zhihu.com/question/450130397/answer/1792335047' \
               '?utm_source=qq&utm_medium=social&utm_oi=605528134699847680'
    resp = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    li = soup.select("img")
    for i in li:
        link = i.attrs["src"]
        if link.startswith("https"):
            real_link = link.split("?")[0]
            download_with_link(real_link)
