# -*- coding: utf-8 -*-

from upload import Upload
from utlis.headers import headers_mp
import time
import os
from confing import Config


class Pub(object):
    def __init__(self, file, session, ydm, config=Config()):
        self.session = session
        self.config = config.config
        self.ydm = ydm
        self.callback = "jQuery32103773561319591048_1534950307354"
        upload = Upload(file, self.session, self.callback)
        self.info = upload.main()
        self.submit = self.submit()

    def get_code(self, url, pid, count):
        resp = self.session.get(url, headers=headers_mp)
        code_name = self.config["path"]["code"].format(pid)
        with open(code_name + '', 'wb') as f:
            for chunk in resp.iter_content(1000):
                f.write(chunk)
        code = self.ydm.get_result(code_name)
        resp_code = self.session.get("http://mp.sina.com.cn/aj/article/verifisendcode?callback={}&sendcode={}&"
                                     "pid={}&_={}".format(self.callback, code, pid, int(time.time() * 1000)),
                                     headers=headers_mp).text
        resp_code_json = eval(resp_code.replace(self.callback, ''))
        if resp_code_json["code"]=="200":
            return True
        else:
            if count>3:
                return False
            resp_code_refresh = self.session.get("http://mp.sina.com.cn/aj/article/refreshsendcode?callback={}&_={}"
                                                 .format(self.callback, int(time.time()*10))).text

            resp_code_refresh_json = eval(resp_code_refresh.replace(self.callback, ''))
            count = count+1
            return self.get_code(resp_code_refresh_json["data"]["codeimg"],resp_code_refresh_json["data"]["pid"],
                                 count)

    def submit(self):
        time.sleep(2)
        url = "http://mp.sina.com.cn/aj/article/checkartsubmit?callback={}&_={}".format(self.callback,
                                                                                        int(time.time()*1000))
        resp_submit = self.session.get(url, headers=headers_mp).text
        if resp_submit:
            rest_submit_status = str(eval(resp_submit.replace(self.callback, ''))["code"])
            if rest_submit_status == "200":
                pass
            if rest_submit_status == "-22":
                return -22
        url_code = "http://mp.sina.com.cn/aj/article/getsendcode?callback={}&_={}".format(self.callback,
                                                                                        int(time.time()*1000))
        resp = self.session.get(url_code, headers=headers_mp).text
        resp_json = eval(resp.replace(self.callback, ''))
        if resp_json["code"] == 200:
            return 200
        if resp_json["code"] == -10:
            code_url = resp_json["data"]["codeimg"]
            pid = resp_json["data"]["pid"]
            code = self.get_code(code_url, pid, 1)
            if code:
                return 200
            else:
                return -10
        else:
            return False

            # self.session.get(code_url)
            # with open()

    def pub(self, article_type, text):
        url = 'http://mp.sina.com.cn/aj/article?type=videosubmit&callback='+ self.callback
        data = {
            "title": self.info[0].split("_")[0],
            "intro": "",
            "ansysWeibo": "0",
            "article_type": article_type,
            "article_smalltype": "0",
            "video_id": self.info[1],
            "file_size": self.info[2],
            "size": self.info[2],
            "file_name": self.info[0],
            "local": "local",
            "headImgSrc": self.info[3]
        }
        if self.submit == -10:
            text.insert('end', "发表视频识别验证码失败\n")
            text.update()
            return 10
        if self.submit == -22:
            text.insert('end', "发文上限\n")
            text.update()
            return 22
        resp = self.session.post(url, headers=headers_mp, data=data).text
        if "success" in resp:
            os.remove(self.info[4])
            os.remove(self.info[5])
            return True
        return False


if __name__ == '__main__':
    from login import Login

    session_ = Login()
    session = session_.login("ikiiea22mn091@qq.com", "lpd666666")["session"]

    print(12313)
    print(session)
    filename = '宋小宝 程野 小品《路口》当时我就把持不住了.mp4'
    a = Pub(filename,session)
    a.pub("22")
