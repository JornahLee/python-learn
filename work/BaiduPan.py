# coding="utf-8"

import requests
import re
import json
import time
import random
from bs4 import BeautifulSoup
# 解决验证码问题，经过测试实际使用过程中不会出验证码，所以没装的话可以屏蔽掉
# import pytesseract
from PIL import Image
from io import BytesIO

'''
初次使用时，请先从浏览器的开发者工具中获取百度网盘的Cookie，并设置在init方法中进行配置，并调用verifyCookie方法测试Cookie的有效性
已实现的方法：
1.获取登录Cookie有效性；
2.获取网盘中指定目录的文件列表；
3.获取加密分享链接的提取码；
4.转存分享的资源；
5.重命名网盘中指定的文件；
6.删除网盘中的指定文件；
7.移动网盘中指定文件至指定目录；
8.创建分享链接；
'''


class BaiDuPan(object):
    """
    传入当前登陆账号的cookie
    """

    def __init__(self, cookie):
        # 创建session并设置初始登录Cookie
        self.session = requests.session()
        # print(re.findall(r'(?<=BDUSS=).+?;', cookie)[0])
        # print(re.findall(r'(?<=STOKEN=).+?;', cookie)[0])
        self.session.cookies['BDUSS'] = re.findall(r'(?<=BDUSS=).+?;', cookie)[0][0:-1]
        self.session.cookies['STOKEN'] = re.findall(r'(?<=STOKEN=).+?;', cookie)[0][0:-1]
        self.headers = {
            'Host': 'pan.baidu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        resp = self.session.get('https://pan.baidu.com/', headers=self.headers).content.decode("utf-8")
        # print(resp)
        info_str = re.findall(r'(?<=locals\.mset\()\{.+?}', resp)[0]
        parse_obj = json.loads(info_str)
        print('初始化获取基本信息。。。。')
        print(parse_obj['username'])
        print(parse_obj['bdstoken'])
        self.bdstoken = parse_obj['bdstoken']
        self.username = parse_obj['username']

    '''
    验证Cookie是否已登录
    返回值errno代表的意思：
    0 有效的Cookie；1 init方法中未配置登录Cookie；2 无效的Cookie
    '''

    def verify_cookie(self):
        if (self.session.cookies['BDUSS'] == '' or self.session.cookies['STOKEN'] == ''):
            return {'errno': 1, 'err_msg': '请在init方法中配置百度网盘登录Cookie'}
        else:
            response = self.session.get('https://pan.baidu.com/', headers=self.headers)
            home_page = response.content.decode("utf-8")
            # print(home_page)
            soup = BeautifulSoup(home_page, 'lxml')
            if ('<title>百度网盘-全部文件</title>' in home_page):
                # user_name = re.findall(r'initPrefetch\((.+?)\'\)', home_page)[0]
                user_name = re.findall(r',"username":.+?"', home_page)[0]
                # user_name = re.findall(r',(?<="username":).+?"', home_page)[0]
                return {'errno': 0, 'err_msg': '有效的Cookie，用户名：%s' % user_name}
            else:
                return {'errno': 2, 'err_msg': '无效的Cookie！'}

    '''
    获取指定目录的文件列表，直接返回原始的json
    '''

    def get_file_list(self, dir='/', order='time', desc=0, page=1, num=100):
        '''
        构造获取文件列表的URL：
        https://pan.baidu.com/api/list?
        bdstoken=  从首页中可以获取到
        &dir=/  需要获取的目录
        &order=name  可能值：name，time，size
        &desc=0  0表示正序，1表示倒序
        &page=  第几页
        &num=100  每页文件数量
        &t=0.8685513844705777  推测为随机字符串
        &startLogTime=1581862647373  时间戳
        &logid=MTU4MTg2MjY0NzM3MzAuMzM2MTAzMzk5MTg3NzYyOQ==  固定值
        &clienttype=0  固定值
        &showempty=0  固定值
        &web=1  固定值
        &channel=chunlei  固定值
        &app_id=250528  固定值
        '''
        t = random.random()
        startLogTime = str(int(time.time()) * 1000)
        url = 'https://pan.baidu.com/api/list?bdstoken=%s&dir=%s&order=%s&desc=%s&page=%s&num=%s&t=%s&startLogTime=%s\
				&logid=MTU4MTg2MjY0NzM3MzAuMzM2MTAzMzk5MTg3NzYyOQ==&clienttype=0&showempty=0&web=1&channel=chunlei&app_id=250528' \
              % (self.bdstoken, dir, order, desc, page, num, t, startLogTime)
        headers = self.headers
        headers['Referer'] = 'https://pan.baidu.com/disk/home?'
        response = self.session.get(url, headers=headers)
        return response.json()

    '''
    获取分享链接的提取码
    返回值errno代表的意思：
    0 提取码获取成功；1 提取码获取失败；
    '''

    @staticmethod
    def get_share_pwd(surl):
        # 云盘精灵的接口
        ypsuperkey_headers = {
            'Host': 'ypsuperkey.meek.com.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        }
        response = requests.get('https://ypsuperkey.meek.com.cn/api/v1/items/BDY-%s?client_version=2019.2' % surl,
                                headers=ypsuperkey_headers)
        pwd = response.json().get('access_code', '')
        if (not pwd):
            # 小鸟云盘搜索接口
            aisou_headers = {
                'Host': 'helper.aisouziyuan.com',
                'Origin': 'https://pan.baidu.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
                'Referer': 'https://pan.baidu.com/share/init?surl=%s' % surl,
            }
            form_data = {
                'url': surl,
                'wrong': 'false',
                'type': 'baidu',
                'v': '3.132',
            }
            response = requests.post('https://helper.aisouziyuan.com/Extensions/Api/ResourcesCode?v=3.132',
                                     headers=aisou_headers, data=form_data)
            pwd = response.text
        errno, err_msg = (0, '提取码获取成功') if pwd else (1, '提取码获取失败：%s' % response.text)
        return {'errno': errno, 'err_msg': err_msg, 'pwd': pwd}

    '''
    识别 验证加密分享时的验证码
    返回值errno代表的意思：
    0 识别成功；1 识别失败；其他值 获取验证码失败；
    '''

    def vcode_OCR(self):
        # 获取验证码
        vcode_res = requests.get(
            'https://pan.baidu.com/api/getcaptcha?prod=shareverify&web=1&channel=chunlei&web=1&app_id=250528&bdstoken=null&clienttype=0',
            headers=self.headers)
        vcode_json = vcode_res.json()
        if (vcode_json['errno'] == 0):
            # 获取验证码图片
            genimage = requests.get(vcode_json['vcode_img'], headers=self.headers)
            # 非自动化脚本，可以改为人工识别，并且将人工识别的验证码保存，用于后续的CNN训练
            vcode_image = BytesIO(genimage.content)
            image = Image.open(vcode_image)
            image.show()
            vcode = input('请输入验证码：')
            f = open('./vcodeImg/%s - %s.jpg' % (vcode, str(int(time.time()) * 1000)), 'wb')
            f.write(genimage.content)
            f.close()

            '''
            将验证码图片加载至内存中进行自动识别
            由于验证码旋转和紧贴，所以导致pytesseract识别率非常底！
            考虑基于CNN深度学习识别，筹备数据集需要一定的时间
            临时解决方案是：识别失败进行重试，加大重试次数
            '''
            # vcode_image = BytesIO(genimage.content)
            # image = Image.open(vcode_image)
            # vcode = pytesseract.image_to_string(image)
            errno, err_msg = (1, '识别失败') if (len(vcode) != 4) else (0, '识别成功')
            vcode_str = vcode_json['vcode_str']
        else:
            errno = vcode_json['errno']
            err_msg = '获取验证码失败'
            vcode_str = ''
        return {'errno': errno, 'err_msg': err_msg, 'vcode': vcode, 'vcode_str': vcode_str}

    '''
    验证加密分享
    返回值errno代表的意思：
    0 加密分享验证通过；1 验证码获取失败；2 提取码不正确；3 加密分享验证失败；4 重试几次后，验证码依旧不正确；
    '''

    def verify_share(self, surl, bdstoken, pwd, referer):
        '''
        构造密码验证的URL：https://pan.baidu.com/share/verify?
        surl=62yUYonIFdKGdAaueOkyaQ  从重定向后的URL中获取
        &t=1572356417593  时间戳
        &channel=chunlei  固定值
        &web=1  固定值
        &app_id=250528  固定值
        &bdstoken=742aa0d6886423a5503bbc67afdb2a7d  从重定向后的页面中可以找到，有时候会为空，经过验证，不要此字段也可以
        &logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==  不知道什么作用，暂时为空或者固定值都可以
        &clienttype=0  固定值
        '''
        t = str(int(time.time()) * 1000)
        url = 'https://pan.baidu.com/share/verify?surl=%s&t=%s&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
				&logid=MTU0ODU4MzUxMTgwNjAuNDg5NDkyMzg5NzAyMzY1MQ==&clienttype=0' % (surl, t, bdstoken)
        form_data = {
            'pwd': pwd,
            'vcode': '',
            'vcode_str': '',
        }
        # 设置重试机制
        is_vcode = False
        for n in range(1, 166):
            # 自动获取并识别验证码，使用pytesseract自动识别时，可加大重试次数
            if is_vcode:
                ocr_result = self.vcode_OCR()
                if (ocr_result['errno'] == 0):
                    form_data['vcode'] = ocr_result['vcode']
                    form_data['vcode_str'] = ocr_result['vcode_str']
                elif (ocr_result['errno'] == 1):
                    continue
                else:
                    return {'errno': 1, 'err_msg': '验证码获取失败：%d' % ocr_result['errno']}
            headers = self.headers
            headers['referer'] = referer
            # verify_json['errno']：-9表示提取码不正确；-62表示需要验证码/验证码不正确（不输入验证码也是此返回值）
            verify_res = self.session.post(url, headers=headers, data=form_data)
            verify_json = verify_res.json()
            if (verify_json['errno'] == 0):
                return {'errno': 0, 'err_msg': '加密分享验证通过'}
            elif (verify_json['errno'] == -9):
                return {'errno': 2, 'err_msg': '提取码不正确'}
            elif (verify_json['errno'] == -62):
                is_vcode = True
            else:
                return {'errno': 3, 'err_msg': '加密分享验证失败：%d' % verify_json['errno']}
        return {'errno': 4,
                'err_msg': '重试多次后，验证码依旧不正确：%d' % (verify_json['errno'] if ("verify_json" in locals()) else -1)}

    '''
    返回值errno代表的意思：
    0 转存成功；1 无效的分享链接；2 分享文件已被删除；
    3 分享文件已被取消；4 分享内容侵权，无法访问；5 找不到文件；6 分享文件已过期
    7 获取提取码失败；8 获取加密cookie失败； 9 转存失败；
    '''

    def save_share(self, url, pwd=None, path='/'):
        share_res = self.session.get(url, headers=self.headers)
        share_page = share_res.content.decode("utf-8")
        '''
        1.如果分享链接有密码，会被重定向至输入密码的页面；
        2.如果分享链接不存在，会被重定向至404页面https://pan.baidu.com/error/404.html，但是状态码是200；
        3.如果分享链接已被删除，页面会提示：啊哦，你来晚了，分享的文件已经被删除了，下次要早点哟。
        4.如果分享链接已被取消，页面会提示：啊哦，你来晚了，分享的文件已经被取消了，下次要早点哟。
        5.如果分享链接涉及侵权，页面会提示：此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问！
        6.啊哦！链接错误没找到文件，请打开正确的分享链接!
        7.啊哦，来晚了，该分享文件已过期
        '''
        if ('error/404.html' in share_res.url):
            return {"errno": 1, "err_msg": "无效的分享链接", "extra": "", "info": ""}
        if ('你来晚了，分享的文件已经被删除了，下次要早点哟' in share_page):
            return {"errno": 2, "err_msg": "分享文件已被删除", "extra": "", "info": ""}
        if ('你来晚了，分享的文件已经被取消了，下次要早点哟' in share_page):
            return {"errno": 3, "err_msg": "分享文件已被取消", "extra": "", "info": ""}
        if ('此链接分享内容可能因为涉及侵权、色情、反动、低俗等信息，无法访问' in share_page):
            return {"errno": 4, "err_msg": "分享内容侵权，无法访问", "extra": "", "info": ""}
        if ('链接错误没找到文件，请打开正确的分享链接' in share_page):
            return {"errno": 5, "err_msg": "链接错误没找到文件", "extra": "", "info": ""}
        if ('啊哦，来晚了，该分享文件已过期' in share_page):
            return {"errno": 6, "err_msg": "分享文件已过期", "extra": "", "info": ""}

        # 提取码校验的请求中有此参数
        # 如果加密分享，需要验证提取码，带上验证通过的Cookie再请求分享链接，即可获取分享文件
        if ('init' in share_res.url):
            surl = re.findall(r'surl=(.+?)$', share_res.url)[0]
            if (pwd == None):
                pwd_result = self.get_share_pwd(surl)
                if (pwd_result['errno'] != 0):
                    return {"errno": 7, "err_msg": pwd_result['err_msg'], "extra": "", "info": ""}
                else:
                    pwd = pwd_result['pwd']
            referer = share_res.url
            verify_result = self.verify_share(surl, self.bdstoken, pwd, referer)
            if (verify_result['errno'] != 0):
                return {"errno": 8, "err_msg": verify_result['err_msg'], "extra": "", "info": ""}
            else:
                # 加密分享验证通过后，使用全局session刷新页面（全局session中带有解密的Cookie）
                share_res = self.session.get(url, headers=self.headers)
                share_page = share_res.content.decode("utf-8")
        # 更新bdstoken，有时候会出现 AttributeError: 'NoneType' object has no attribute 'group'，重试几次就好了
        info_str = re.findall(r'(?<=locals\.mset\()\{.+?}\)', share_page)[0]
        parse_obj = json.loads(info_str[0:-1])
        bdstoken = parse_obj['bdstoken']
        shareid = parse_obj['shareid']
        _from = parse_obj['share_uk']
        '''
        构造转存的URL，除了logid不知道有什么用，但是经过验证，固定值没问题，其他变化的值均可在验证通过的页面获取到
        '''
        save_url = 'https://pan.baidu.com/share/transfer?shareid=%s&from=%s&ondup=newcopy&async=1&channel=chunlei&web=1&app_id=250528&bdstoken=%s\
					&logid=MTU3MjM1NjQzMzgyMTAuMjUwNzU2MTY4MTc0NzQ0MQ==&clienttype=0' % (shareid, _from, bdstoken)
        file_list = parse_obj['file_list']
        form_data = {
            # 这个参数一定要注意，不能使用['fs_id', 'fs_id']，谨记！
            'fsidlist': '[' + ','.join([str(item['fs_id']) for item in file_list]) + ']',
            'path': path,
        }
        headers = self.headers
        headers['Origin'] = 'https://pan.baidu.com'
        headers['referer'] = url
        '''
        用带登录Cookie的全局session请求转存
        如果有同名文件，保存的时候会自动重命名：类似xxx(1)
        暂时不支持超过文件数量的文件保存
        '''
        save_res = self.session.post(save_url, headers=headers, data=form_data)
        save_json = save_res.json()
        errno, err_msg, extra, info = (0, '转存成功', save_json['extra'], save_json['info']) if (
                save_json['errno'] == 0) else (9, '转存失败：%d' % save_json['errno'], '', '')
        return {'errno': errno, 'err_msg': err_msg, "extra": extra, "info": info}

    '''
    重命名指定文件
    0 重命名成功；1 重命名失败；
    '''

    def rename(self, path, newname):
        '''
        构造重命名的URL：https://pan.baidu.com/api/filemanager?
        bdstoken=  从首页可以获取到
        &opera=rename  固定值
        &async=2  固定值
        &onnest=fail  固定值
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        '''
        response = self.session.get('https://pan.baidu.com/', headers=self.headers)
        bdstoken = re.findall(r'initPrefetch\(\'(.+?)\'\,', response.content.decode("utf-8"))[0]
        url = 'https://pan.baidu.com/api/filemanager?bdstoken=%s&opera=rename&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528\
				&logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % bdstoken
        form_data = {"filelist": "[{\"path\":\"%s\",\"newname\":\"%s\"}]" % (path, newname)}
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '重命名成功！'}
        else:
            return {'errno': 1, 'err_msg': '重命名失败！', 'info': response.json()}

    '''
    删除指定文件
    0 删除成功；1 删除失败；
    '''

    def delete(self, path):
        '''
        构造重命名的URL：https://pan.baidu.com/api/filemanager?
        bdstoken=  从首页可以获取到
        &opera=delete  固定值
        &async=2  固定值
        &onnest=fail  固定值
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        '''
        url = 'https://pan.baidu.com/api/filemanager?bdstoken=%s&opera=delete&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528\
				&logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % self.bdstoken
        form_data = {"filelist": "[\"%s\"]" % path}
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '删除成功！'}
        else:
            return {'errno': 1, 'err_msg': '删除失败！', 'info': response.json()}

    '''
    移动文件至指定目录
    0 删除成功；1 删除失败；
    '''

    def move(self, path, destination, newname=False):
        '''
        构造重命名的URL：https://pan.baidu.com/api/filemanager?
        bdstoken=  从首页可以获取到
        &opera=move  固定值
        &async=2  固定值
        &onnest=fail  固定值
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        '''
        response = self.session.get('https://pan.baidu.com/', headers=self.headers)
        bdstoken = re.findall(r'initPrefetch\(\'(.+?)\'\,', response.content.decode("utf-8"))[0]
        url = 'https://pan.baidu.com/api/filemanager?bdstoken=%s&opera=move&async=2&onnest=fail&channel=chunlei&web=1&app_id=250528\
				&logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % bdstoken
        if (not newname):
            newname = path.split('/')[-1]
        form_data = {
            "filelist": "[{\"path\":\"%s\",\"dest\":\"%s\",\"newname\":\"%s\"}]" % (path, destination, newname)}
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '移动成功！'}
        else:
            return {'errno': 1, 'err_msg': '移动失败！', 'info': response.json()}

    '''
    随机生成4位字符串
    '''

    @staticmethod
    def generate_pwd(n=4):
        pwd = ""
        for i in range(n):
            temp = random.randrange(0, 3)
            if temp == 0:
                ch = chr(random.randrange(ord('A'), ord('Z') + 1))
                pwd += ch
            elif temp == 1:
                ch = chr(random.randrange(ord('a'), ord('z') + 1))
                pwd += ch
            else:
                pwd = str((random.randrange(0, 10)))
        return pwd

    '''
    创建分享链接
    fid_list为列表，例如：[1110768251780445]
    0 创建成功；1 创建失败；
    '''

    def create_share_link(self, fid_list, period=0, pwd=False):
        '''
        构造重命名的URL：https://pan.baidu.com/share/set?
        bdstoken=  从首页可以获取到
        &channel=chunlei  固定在
        &web=1  固定值
        &app_id=250528  固定值
        &logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==  固定值
        &clienttype=0  固定值
        '''
        url = 'https://pan.baidu.com/share/set?bdstoken=%s&channel=chunlei&web=1&app_id=250528\
				&logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % self.bdstoken
        if (not pwd):
            pwd = self.generate_pwd()
        '''
        schannel=4  不知道什么意思，固定为4
        channel_list=[]  不知道什么意思，固定为[]
        period=0  0表示永久，7表示7天
        pwd=w4y5  分享链接的提取码，可自定义
        fid_list=[1110768251780445]  分享文件的id列表，可调用getFileList方法获取文件列表，包含fs_id
        '''
        form_data = {
            'schannel': 4,
            'channel_list': '[]',
            'period': period,
            'pwd': pwd,
            'fid_list': str(fid_list),
        }
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '创建分享链接成功！', 'info': {'link': response.json()['link'], 'pwd': pwd}}
        else:
            return {'errno': 1, 'err_msg': '创建分享链接失败！', 'info': response.json()}

    def create_dir(self, pathname):
        '''
        参考 move方法
        '''
        url = 'https://pan.baidu.com/api/create?' \
              'a=commit&channel=chunlei&web=1&app_id=250528&bdstoken=%s' \
              '&logid=MTU4MTk0MzY0MTQwNzAuNDA0MzQxOTM0MzE2MzM4Ng==&clienttype=0' % self.bdstoken
        form_data = {"path": pathname, "isdir": 1, "block_list": []}
        response = self.session.post(url, headers=self.headers, data=form_data)
        if (response.json()['errno'] == 0):
            return {'errno': 0, 'err_msg': '创建目录成功！'}
        else:
            return {'errno': 1, 'err_msg': '创建目录失败！', 'info': response.json()}

    def get_total_size(self):
        """
        获取当前账号基本信息
        是否会员过期
        是否为免费用户
        总共容量, 单位byte
        已使用容量, 单位byte
        """
        url = "https://pan.baidu.com/api/quota?" \
              "checkexpire=1&checkfree=1&channel=chunlei&web=1&app_id=250528" \
              "&bdstoken=c0487249e7304af871a5673da8508a22&logid=RkQyNTFGRTYyQTE0QUEwQjY5QTg2QTNFN0Y4RkMzQzU6Rkc9MQ==" \
              "&clienttype=0"
        resp = self.session.get(url, headers=self.headers)
        info = json.loads(resp.text)
        return {"total": info['total'], 'used': info['used']}


def main():
    cookie = 'BIDUPSID=C92F406CEACAB4768D6E102D1D7D138C; PSTM=1619435971; __yjs_duid=1_24652996423433c6fac03828ec50d61b1619439208725; pan_login_way=1; PANWEB=1; MCITY=-75:; csrfToken=Y38B9gZ4hmS2ZwLIcdZPwTyY; Hm_lvt_fa0277816200010a74ab7d2895df481b=1639800377; Hm_lpvt_fa0277816200010a74ab7d2895df481b=1639800487; BAIDUID=FD251FE62A14AA0B69A86A3E7F8FC3C5:FG=1; BDCLND=NSCcU4kDz3r341fO/rYYSXZBOmBq0+88K9Z2XnLJ0V8=; delPer=0; BAIDUID_BFESS=FD251FE62A14AA0B69A86A3E7F8FC3C5:FG=1; PSINO=2; ZD_ENTRY=baidu; BAIDU_WISE_UID=wapp_1640101982808_568; BCLID=8632690060128000410; BDSFRCVID=mWDOJexroG04LNRHz03IMGbdBdNbUdrTDYrEQ-mAp1wm6V8VJeC6EG0Pts1-dEu-EHtdogKKXgOTHw0F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tbCjoCP2tC83qJomjKTVhPDO5fneetJyaR3C5qQvWJ5TMCo6X-rAbhDnMP5mt5jvJg7xQCjIbl3DShPC-tPbMTFEMn5RQUR-bCoO0l7V3l02VMO9e-t2yT0VKx7LK4RMW23v0h7mWP02sxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjCKjTJLeH-HtTnfb5kXWnTaanTHDR3n-tTVhnQH-UnLqbcl3eOZ0l8Kttn8enja-U7OL6KRDRAJ3Mb72IL8VUomWIQHDUTDBpKaylKwMboaQlcTt2j4KKJxB4PWeIJoLt5F0T01hUJiBhvMBan7LKJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC8mD6LajjQBep78tK6Bb6Q0XnT8MR7_eTrnhPF3Mq3QXP6-35KHyDrphCblWIjxsfOVMtI5KPr0MHO8Ql37JD6y0CLhatoKbKbhQhQNKRIy-toxJpO3BRbMopvaBl7Foh5vbURvW--g3-7fJU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-j5JIEoK--tCDhMDLr2bubq4I02xrOa468aKoMsJOOaCkVHqvOy4oTj6Dl-RjkJTQ7tGn4bqTVaDO5MIQyDqr_3MvB-fPeQpOUtHRPQhP2LljKJ4OPQft20-kIeMtjBbQuB2ovKR7jWhviep72ybt2QlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDqbOKatoa3RTeb6rjDnCrhqJUXUI82h5y058JBgoNaPFMthTYsnogL4OF-lLOKRORXRj4L4jL54thbbC-SCnKy4oTjxL1Db3Jb5_L5gTtsl5dbnboepvoW-Jc3MkWD-jdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEK5r2SCKatKPa3H; BCLID_BFESS=8632690060128000410; BDSFRCVID_BFESS=mWDOJexroG04LNRHz03IMGbdBdNbUdrTDYrEQ-mAp1wm6V8VJeC6EG0Pts1-dEu-EHtdogKKXgOTHw0F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tbCjoCP2tC83qJomjKTVhPDO5fneetJyaR3C5qQvWJ5TMCo6X-rAbhDnMP5mt5jvJg7xQCjIbl3DShPC-tPbMTFEMn5RQUR-bCoO0l7V3l02VMO9e-t2yT0VKx7LK4RMW23v0h7mWP02sxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjCKjTJLeH-HtTnfb5kXWnTaanTHDR3n-tTVhnQH-UnLqbcl3eOZ0l8Kttn8enja-U7OL6KRDRAJ3Mb72IL8VUomWIQHDUTDBpKaylKwMboaQlcTt2j4KKJxB4PWeIJoLt5F0T01hUJiBhvMBan7LKJIXKohJh7FM4tW3J0ZyxomtfQxtNRJ0DnjtnLhbC8mD6LajjQBep78tK6Bb6Q0XnT8MR7_eTrnhPF3Mq3QXP6-35KHyDrphCblWIjxsfOVMtI5KPr0MHO8Ql37JD6y0CLhatoKbKbhQhQNKRIy-toxJpO3BRbMopvaBl7Foh5vbURvW--g3-7fJU5dtjTO2bc_5KnlfMQ_bf--QfbQ0hOhqP-j5JIEoK--tCDhMDLr2bubq4I02xrOa468aKoMsJOOaCkVHqvOy4oTj6Dl-RjkJTQ7tGn4bqTVaDO5MIQyDqr_3MvB-fPeQpOUtHRPQhP2LljKJ4OPQft20-kIeMtjBbQuB2ovKR7jWhviep72ybt2QlRX5q79atTMfNTJ-qcH0KQpsIJM5-DWbT8EjHCDqbOKatoa3RTeb6rjDnCrhqJUXUI82h5y058JBgoNaPFMthTYsnogL4OF-lLOKRORXRj4L4jL54thbbC-SCnKy4oTjxL1Db3Jb5_L5gTtsl5dbnboepvoW-Jc3MkWD-jdJJQOBKQB0KnGbUQkeq8CQft20b0EeMtjW6LEK5r2SCKatKPa3H; BDUSS=83dFNoOW81ZDVIMjdndlFZWlR5UXJ0NHRqWUV6N01mV0ZlSnFnbFlpbnNGdlJoSVFBQUFBJCQAAAAAAQAAAAEAAACu-jBWtPPOsrDNM2hhbwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOyJzGHsicxhZ0; BDUSS_BFESS=83dFNoOW81ZDVIMjdndlFZWlR5UXJ0NHRqWUV6N01mV0ZlSnFnbFlpbnNGdlJoSVFBQUFBJCQAAAAAAQAAAAEAAACu-jBWtPPOsrDNM2hhbwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOyJzGHsicxhZ0; STOKEN=b340c83787b192c191fa95ed49b60eaa294e6298f7227c7b681e8d0f1cb59ba0; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=35638_35106_31254_35457_34584_35490_35246_35695_35642_35317_26350_35474_35558; BA_HECTOR=ak2080840hal258ljv1gsvfrp0q; Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1639826119,1639887955,1641004399,1641004972; Hm_lpvt_7a3960b6f067eb0085b7f96ff5e660b0=1641004972; PANPSC=17168378876267144570:Kkwrx6t0uHD8oUc/y89Y3BoU7DKe/cDJPte2imWG2X7Ld28VUR8tXXpR1A/QFbfQh8e57zgMOk4TOHQ48QXZaTEtb2PuZJw8D+WzhDuLxuKhdffKqBGRN96meYGUss/GjTSP66eFQ9ExrmmQowLs1mKmXcvc2dd5a7opy+Oal1MBq4RltvI7LWtd3K3d2bgIJDCABb9nWGTrbkBUnMiFfw==; ndut_fmt=7D856246A5BFD8CEC01CA9FBB95701B6E87F83B06C983A6FBA4A1C352E60A7BC'
    baidu = BaiDuPan(cookie)
    print(baidu.get_total_size())
    # print(baidu.getFileList(dir='/A GAME'))
    # print(baidu.delete("/不要的"))
    # print(baidu.createShareLink(fid_list=[476888690961731],period=7))
    # 'https://pan.baidu.com/s/1XelJBczwkNAJ1kMIrwgwXg', 'pwd': 'Xezr'}
    # 链接: https://pan.baidu.com/s/190A5Dfga9LnHvtsmir0YzA 提取码: w74u 复制这段内容后打开百度网盘手机App，操作更方便哦
    # print(baidu.saveShare('https://pan.baidu.com/s/190A5Dfga9LnHvtsmir0YzA', 'w74u', '/taobao'))
    # print(baidu.create_dir('/data2'))


if __name__ == '__main__':
    main()
