# -*- coding: utf-8 -*-

import rsa
import binascii
import time
from confing import Config
import math
import random
import requests
from urllib.parse import quote_plus
import base64
from utlis.utils import log


class Login(object):
    def __init__(self, ydm, config=Config()):
        self.config = config.config
        self.ydm = ydm
        self.session = requests.session()
        self.proxy = self.config["proxy"]["ip"]
        if self.proxy:
            self.session.proxies = {'http': self.proxy, 'https': self.proxy}
        self.headers = dict(self.config.items('header'))
        self.proxy = ''
        self.login_url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_='+\
                         str(int(time.time() * 1000))

    # 获取加密后的密码
    @staticmethod
    def get_password(password, server_time, nonce, pubkey):
        public_key = int(pubkey, 16)
        key = rsa.PublicKey(public_key, 65537)
        message = str(server_time) + '\t' + str(nonce) + '\n' + str(password)
        message = message.encode("utf-8")
        password = binascii.b2a_hex(rsa.encrypt(message, key))
        return password

    def get_code(self,path):

        return self.ydm.get_result(path)

    # 获取验证码地址
    @staticmethod
    def get_code_url(p_cid):
        size = 0
        url = "http://login.sina.com.cn/cgi/pin.php"
        pin_code_url = '{}?r={}&s={}&p={}'.format(url, math.floor(random.random() * 100000000), size, p_cid)
        return pin_code_url

    # 获取验证码图片
    def get_code_img(self, username):

        url = "http://login.sina.com.cn/cgi/pin.php?rnd="+str(int(time.time() * 1000))
        code = self.config["path"]["code"]
        code_name = code.format(username)
        resp = self.session.get(url, headers=self.headers, stream=True)
        with open(code_name, 'wb') as f:
            for chunk in resp.iter_content(1000):
                f.write(chunk)
        return code_name

    # 获取用户名
    @staticmethod
    def get_name(name):
        # name must be string
        username_quote = quote_plus(str(name))
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    # 获取服务器返回信息
    def get_server_data(self, su):
        url = "https://login.sina.com.cn/sso/prelogin.php?entry=account&callback=sinaSSOController.preloginCallBack&su="
        pre_url = url + su + "&rsakt=mod&client=ssologin.js(v1.4.15)&_=" + str(int(time.time() * 1000))
        pre_data_res = self.session.get(pre_url, headers=self.headers)
        server_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))
        return server_data

    # 登录参数,构造请求
    def login_data(self, name, password, door=''):
        su = self.get_name(name)
        server_data = self.get_server_data(su)
        server_time = server_data["servertime"]
        nonce = server_data['nonce']
        rsakv = server_data["rsakv"]
        pubkey = server_data["pubkey"]
        sp = self.get_password(password, server_time, nonce, pubkey)

        data = {
            'cdult': '3',
            'domain': 'sina.com.cn',
            'encoding': 'UTF-8',
            'entry': 'account',
            'from': '',
            'gateway': '1',
            'nonce': nonce,
            "door": door,
            "vsnval":"",
            'pagerefer': "https://www.baidu.com/link?url=SvjgN-tDkogaOMT4yoW3HJ9H8bNLimP7oAJK_wXz1Nq&wd=&eqid=a6d4bd0500021e50000000025b6d951e",
            'prelt': 34,
            'pwencode': 'rsa2',
            "returntype": "TEXT",
            'rsakv': rsakv,
            'savestate': '30',
            'servertime': server_time,
            'service': 'sso',
            'sp': sp,
            'sr': '1536*864',
            'su': su,
            'useticket': '0',
            'vsnf': '1',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack'
        }
        return data

    def status(self):
        if "账号信息" in self.session.get("http://mp.sina.com.cn/#/Home/Notice", headers=self.headers).text:
            return True
        return False

    def get_login_status(self, resp, username):
        if resp['retcode'] == '0':
            log('debug', '账号({})登录成功'.format(username))
            return {'username': username, 'session': self.session, 'code': 0}
        if resp['retcode'] == '101':
            log("error", '账号({})或密码错误'.format(username))
            return {'username': username, 'session': self.session, 'code': 101}
        if resp["retcode"] == '2089':
            log('error', '登录保护触发')
            return {'username': username, 'session': self.session, 'code': 2089}
        if resp["retcode"] == '4049' or '2070':
            log('debug', '使用验证码登录')
            return {'username': username, 'session': self.session, 'code': 4049}

    def login(self, username, password, cookie=""):
        if cookie:
            cookie_jar = requests.utils.cookiejar_from_dict({"Cookie": cookie}, cookiejar=None, overwrite=True)
            self.session.cookies = cookie_jar
            if self.status():
                return {'username': username, 'session': self.session, 'code': 0}
            else:
                raise Exception("登录失败")

        data = self.login_data(username, password)
        resp = self.session.post(self.login_url, data=data, headers=self.headers).json()
        status = self.get_login_status(resp, username)
        if status["code"] == 4049:
            # 如果需要验证码，则给三次机会登录
            for i in range(3):
                img_path = self.get_code_img(username)
                code = self.get_code(img_path)
                data = self.login_data(username, password, code)
                resp = self.session.post(self.login_url, data=data, headers=self.headers).json()
                status = self.get_login_status(resp, username)
                if status["code"] == 0:
                    return status
            return status
        return status

if __name__ == '__main__':
    a = Login()
    account = '''18135693663|lpd888888|SINAGLOBAL=114.243.171.239_1533819077.937983; SCF=AgUiCTRFjBDklduKOvWJvTO2nWSgcGA4N2N5sAorLl_N1I4lPevLLnRET-As8MUxWb8nR6eKEa4XwLKLA28fopA.; sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLaMs4yxjbOguY2jhLeJp5WpmYO0toyzjLGNs6C5jaOEtw==; SUB=_2A252apcEDeRhGeBN6FMW-CfKyjuIHXVVlDlMrDV_PUNbm9AKLVnAkW1NRGqABFvEONiQWj2OM7_uwZ4LwpYV_1KB; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whgo1_ANAHykQHL2Ecj0z3A5NHD95Qce0epS0n4So2NWs4Dqcj.i--fi-ihiKn7i--fi-isiKn0i--Ni-8hiK.pi--fi-zNi-zX; ALF=1565530836; timeNumber=5113316; timestamp=51133160033WrSXqPxfM725Ws9jqgMF55529P9D9Whgo1_ANAHykQHL2Ecj0z3A5NHD95Qce0epS0n4So2NWs4Dqcj.i--fi-ihiKn7i--fi-isiKn0i--Ni-8hiK.pi--fi-zNi-zX; Apache=114.243.171.225_1533994837.959519; mptrace=L2dPODJpU1VoTFkvamhlNytyekFiemNabU5LcjErWmo3M3pINm05eWlYWkg4cWtzSXhkT25EaG8rT2VZMUhSRQ==; mp_sendArt=bGtsaXVnZjNjMmpreVNPbHFPODlWTWtzZzV6S3J4V3o4cXF2UVBXUjhWRT0='''
    print(a.login("ikiiea22mn091@qq.com", "lpd666666"))






