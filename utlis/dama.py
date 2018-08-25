# coding:utf-8
import json, time, requests
from confing import Config


class YDMHttp(object):

    def __init__(self, text=''):
        self.apiurl = 'http://api.yundama.com/api.php'
        config = Config()
        self.config = config.config
        self.username = self.config["ydm"]["username"]
        self.password = self.config["ydm"]["password"]
        self.appid = self.config["ydm"]["appid"]
        self.appkey = self.config["ydm"]["appkey"]
        self.text = text
        self.login()

    def __new__(cls, *args, **kwargs):
        if not hasattr(YDMHttp, "_instance"):
            YDMHttp._instance = object.__new__(cls)
        return YDMHttp._instance

    def request(self, fields, files=[]):
        response = self.post_url(self.apiurl, fields, files)
        response = json.loads(response)
        return response

    def login(self):
        data = {'method': 'login', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey}
        response = self.request(data)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['uid']
        else:
            return -9001

    def upload(self, filename, code_type, timeout):
        data = {'method': 'upload', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'codetype': str(code_type), 'timeout': str(timeout)}
        file = {'file': filename}
        response = self.request(data, file)
        if response:
            if response['ret'] and response['ret'] < 0:
                return response['ret']
            else:
                return response['cid']
        else:
            return -9001

    def result(self, cid):
        data = {'method': 'result', 'username': self.username, 'password': self.password, 'appid': self.appid,
                'appkey': self.appkey, 'cid': str(cid)}
        response = self.request(data)
        return response and response['text'] or ''

    def decode(self, filename, code_type, timeout):
        cid = self.upload(filename, code_type, timeout)
        if cid > 0:
            for i in range(0, timeout):
                result = self.result(cid)
                if result != '':
                    return cid, result
                else:
                    time.sleep(1)
            return -3003, ''
        else:
            return cid, ''

    @staticmethod
    def post_url(url, fields, files=[]):
        for key in files:
            files[key] = open(files[key], 'rb')
        res = requests.post(url, files=files, data=fields)
        return res.text

    def get_result(self,filename):
        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = self.decode(filename, self.config["ydm"]["codetype"], 60)
        if self.text:
            self.text.insert('end', "识别的验证码为{}\n".format(result))
            self.text.update()
        return result


if __name__ == '__main__':
    a = YDMHttp()
    a.get_result("D:\\weibo\\png\\ikiiea22mn091@qq.com.png")