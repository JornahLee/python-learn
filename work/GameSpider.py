import requests  # pip3 install requests
from bs4 import BeautifulSoup  # pip3 install beautifulsoup4,依赖pip3 install lxml
import re
import traceback
from DbHelper import DbHelper

db = DbHelper(None, None, None, None)


class GameSpider:
    def __init__(self, cookie, db_util):
        self.headers = {
            # 存储任意的请求头信息
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0)'
                          ' AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'cookie': cookie
        }
        self.db_util = db_util

    def get_baidu_url_and_code(self, url: str):
        resp = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(resp.text, "lxml")
        res = soup.select('.pwd > span')
        baidu_url = ''
        code = ''
        if len(res) > 0:
            code = res[0].text
            print(code)
        else:
            print('no pwd')

        res2 = soup.select('.pay-box > a')
        if len(res2) > 0:
            print(res2[0].attrs['href'])
            resp = requests.get(res2[0].attrs['href'], headers=self.headers)
            baidu_url = re.findall(r"(?<=location=').+?'", resp.text)[0][0:-1]
            print(url)
        else:
            print('no share url')

        res3 = soup.select('.list-paybody')
        activation_code_list = ''
        if len(res3) > 0:
            activation_code_list = res3[0].text
        return {"code": code, "url": baidu_url, "activation_code": str(activation_code_list)}
        pass

    def get_game_by_page(self, page_num: int):
        page_url = 'https://86000k.com/q/page/%d/' % page_num
        resp = requests.get(page_url, headers=self.headers)
        soup = BeautifulSoup(resp.text, "lxml")
        for i in soup.find_all("div", attrs={'class': 'entry-wrapper'}):
            for x in i.select("h2"):
                name = x.find('a').text
                print(name)
                url = x.find('a').attrs['href']
                print(url)
                self.db_util.insert("insert into game(name,url) values('%s','%s')" % (name, url))
        pass

    def save(self):
        sql = 'select * from game where share_link is null order by id desc limit 100'
        update_url_code_sql = "update game set share_link='%s',share_code='%s',activation_code='%s' where id =%s"
        # 元组形式返回数据库记录
        for game in self.db_util.query(sql):
            try:
                print(game['name'])
                print(game['url'])
                baidu_share_result = self.get_baidu_url_and_code(game['url'])
                self.db_util.update(update_url_code_sql % (
                    baidu_share_result['url'], baidu_share_result['code'], baidu_share_result['activation_code'],
                    game['id']))
                self.db_util.commit()
            except Exception as ex:
                print('<<<<')
                traceback.print_exc()
                print(str(ex))
                print('>>>>')
                # print(ex)


