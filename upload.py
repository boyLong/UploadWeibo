# -*- coding: utf-8 -*-

import time
import requests
from utlis.headers import *
from utlis.utils import *
import os
from confing import Config
from requests_toolbelt.multipart.encoder import MultipartEncoder


class Upload(object):
    def __init__(self, filename, session, callback):
        config = Config()
        self.config = config.config
        self.last_mod = int(time.time() * 1000) - 1111111
        self.session = session
        self.callback = callback           # 'jQuery32109369954281154376_1533994871267'
        self.url_auth = 'http://mp.sina.com.cn/aj/vms/gets3authurl'
        self.png, self.video, self.t, self.title = self.file_path(filename)
        self.video_size = self.get_size(self.video)
        self.video_id = self.get_id()


    @staticmethod
    def get_size(path):
        return os.path.getsize(path)

    @staticmethod
    def get_upload_id(url):
        requests.options(url, headers=headers_op("POST"))
        resp = requests.post(url, headers=headers_up()).json()
        return resp["UploadId"]

    @staticmethod
    def get_parts(url):
        resp = requests.get(url, headers=headers_get_up()).json()
        data = []
        for i in resp["Parts"]:
            data.append('{"PartNumber":%s,"ETag":"%s"}' % (i["PartNumber"], i["ETag"]))
        parts = '[' + ",".join(data) + ']'
        return parts

    def file_path(self, filename):
        t = ("_" + str(int(time.time()*1000)) + '.').join(filename.split('.'))
        return self.config["path"]["png"]+'{}.png',  self.config["path"]["video"] + filename, t.replace("，",''), t

    # 获取videoID
    def get_id(self):
        param = {
            "callback": self.callback,
            "size": self.video_size,
            "t": self.t,
            "is_upload": 2,
            "lastModified": self.last_mod,
            "_": int(time.time()*1000)
        }
        resp = self.session.get('http://mp.sina.com.cn/aj/vms/upurl', params=param, headers=headers_mp)
        null = None
        resp_json = (eval(resp.text.replace(self.callback, '')))
        return resp_json['data']["video_id"]

    def post_auth_url(self):
        param = {
            "callback": self.callback,
            "uri": self.t+"?multipart",
            "verb": "POST",
            "content_type": "application/octet-stream",
            "lastModified": int(time.time()*1000),
            "_": int(time.time()*1000)
        }
        resp = self.session.get(self.url_auth, params=param, headers=headers_mp)
        resp_json = (eval(resp.text.replace(self.callback, '')))
        authenticated = resp_json["data"]["authenticated_URL"].replace("\/", '/') + "&formatter=json"
        return authenticated

    def put_auth_url(self, number, upload_id):
        param = {
            "callback": self.callback,
            "uri": self.t+"?partNumber={}&uploadId={}".format(number, upload_id),
            "verb": "PUT",
            "content_type": "application/octet-stream",
            "_": int(time.time()*1000)
        }
        resp = self.session.get(self.url_auth, params=param, headers=headers_mp)
        resp_json = (eval(resp.text.replace(self.callback, '')))
        authenticated = resp_json["data"]["authenticated_URL"].replace("\/", '/') + "&formatter=json"
        return authenticated

    def get_auth_url(self, upload_id):
        param = {
            "callback": self.callback,
            "uri": self.t + "?uploadId={}".format(upload_id),
            "verb": "GET",
            "_":  int(time.time()*1000),
        }
        resp = self.session.get(self.url_auth, params=param, headers=headers_mp)
        resp_json = (eval(resp.text.replace(self.callback, '')))
        authenticated = resp_json["data"]["authenticated_URL"].replace("\/", '/') + "&formatter=json"
        return authenticated

    def post_auth_json(self, upload_id):
        param = {
            "callback": self.callback,
            "uri": self.t + "?uploadId={}".format(upload_id),
            "verb": "POST",
            "content_type": "application/json",
            "_": int(time.time() * 1000)
        }
        resp = self.session.get(self.url_auth, params=param, headers=headers_mp)
        resp_json = (eval(resp.text.replace(self.callback, '')))
        authenticated = resp_json["data"]["authenticated_URL"].replace("\/", '/') + "&formatter=json"
        return authenticated

    @staticmethod
    def res_upload(url, parts):
        requests.options(url, headers=headers_op("POST"))

        requests.post(url, headers=headers_res(), data=parts)

    @retry
    def upload_png(self):
        png = self.png.format(self.video_id)
        screen_shot(self.video, png)
        with open(png, 'rb') as f:
            file = f.read()
        multipart_encoder = MultipartEncoder(
            fields={
                'img':  ("blob", file, 'image/png')
            },
            boundary='WebKitFormBoundary3g09JC8HaMLMBv21'
        )

        resp = self.session.post('http://mp.sina.com.cn/aj/upload?type=article&json=1', headers=header_png(self.get_size(png)),
                                 data=multipart_encoder).json()
        png_url = resp["data"]
        if png_url:
            return resp["data"]
        else:
            raise Exception(u"上传图片失败")

    def get_list(self):
        time.sleep(2)
        url = "http://mp.sina.com.cn/aj/activity/list?_callback={}&articleType=3&_={}".format(self.callback,
                                                                                              int(time.time()*1000))
        self.session.get(url, headers=headers_mp)

    def upload_file(self, url, file):
        requests.options(url, headers=headers_op("PUT"))
        requests.put(url, headers=headers_up(self.get_size(self.video), "put"), data=file)

    def upload(self, upland_id):
        with open(self.video, 'rb') as f:
            number = 1
            while 1:
                file = f.read(31457280)
                if not file:
                    break
                put_url = self.put_auth_url(number, upland_id)
                self.upload_file(put_url, file)
                number += 1

    def main(self):
        """
        主运行程序，首先使用post_auth_url函数post请求，获取一个可以得到upland的url，
        使用此url进行option以及post请求，获取到upland_id，
        接下来使用获取到的upland_id获取到可以上传视频的地址
        对此地址进行option以及put上传视频，
        接下来使用get_auth_url方法获取到可以获取etag的url，并使用get_etag获取etag
        获取可以上传etag的url
        上传etag
        """
        # 获取视频上传的id
        url = self.post_auth_url()
        upland_id = self.get_upload_id(url)

        # 上传视频
        self.upload(upland_id)
        png = self.upload_png()  # 上传封面截图

        #  开始获取每段视频对应的 Etag
        url = self.get_auth_url(upland_id)
        parts = self.get_parts(url)

        # 上传每段etag
        url = self.post_auth_json(upland_id)
        self.res_upload(url, parts)
        self.get_list()
        return self.title,  self.video_id, self.video_size, png, self.video, self.png.format(self.video_id)


if __name__ == '__main__':
    a=Upload('黄磊简直戏精，小猪刚沉浸在胜利喜悦中，听清状况瞬间悲伤到狂笑.mp4')
    print(a.upload_png())
