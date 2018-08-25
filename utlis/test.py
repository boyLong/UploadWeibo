import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

# querystring = {"type":"article^","json
headers = {
    "Host":	"mp.sina.com.cn",
    'Accept': "*/*",
    'Origin': "http://mp.sina.com.cn",
    'X-Requested-With': "XMLHttpRequest",

    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400",
    'Content-Type': "multipart/form-data; boundary=----WebKitFormBoundary81Byq41cBEyB4uw5",
    'Referer': "http://mp.sina.com.cn/main/editor?vt=4",
    'Accept-Encoding': "gzip, deflate",
    'Accept-Language': "zh-CN,zh;q=0.9",
    "Cookie": "SINAGLOBAL=114.243.171.239_1533819077.937983; SCF=AgUiCTRFjBDklduKOvWJvTO2nWSgcGA4N2N5sAorLl_N1I4lPevLLnRET-As8MUxWb8nR6eKEa4XwLKLA28fopA.; sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLaMs4yxjbOguY2jhLeJp5WpmYO0toyzjLGNs6C5jaOEtw==; SUB=_2A252apcEDeRhGeBN6FMW-CfKyjuIHXVVlDlMrDV_PUNbm9AKLVnAkW1NRGqABFvEONiQWj2OM7_uwZ4LwpYV_1KB; ALF=1565530836; mptrace=VVQ4eTh4eWw2UTl3N0hIUkhlWnpHVW5SSzNocjBuSnZpaitUMzgwcnd3STNhVWlHcFFHdGtJQmx6V3lOS0RPTg%3D%3D; mp_sendArt=eVlBR0xpeVFCWG13SDhUcnRtS1hvV1lwSDY1VGZFc1NuRHR5dTFBYk9Tbz0%3D; Apache=114.243.171.225_1534251061.266205",
    "Connection": "keep-alive"
}
headers_1 = {
    'Pragma': "no-cache",
    'origin': "http://mp.sina.com.cn",
    'accept-encoding': "gzip, deflate",
    'accept-language': "zh-CN,zh;q=0.9",
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5702.400 QQBrowser/10.2.1893.400",
    'content-type': "multipart/form-data; boundary=WebKitFormBoundary3dWjYmkrbDNtHpUT",
    'accept': "*/*",
    'cache-control': "no-cache",
    'x-requested-with': "XMLHttpRequest",
    'proxy-connection': "keep-alive",
    'referer': "http://mp.sina.com.cn/main/editor?vt=4",
    }
# response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
url = 'http://n.sinaimg.cn/sinacn21/750/w480h270/20180811/30aa-hhqtaww9821466.png'
import base64

with open("D:\\weibo\\png\\13.png", 'rb') as f:
    file = f.read()
multipart_encoder = MultipartEncoder(
            fields={
                'img':  ("blob", file, 'image/png')
            },
            boundary='------WebKitFormBoundary3dWjYmkrbDNtHpUT'
        )
print(requests.post('http://mp.sina.com.cn/aj/upload?type=article&json=1', headers=headers_1,
                                data=multipart_encoder).json())
