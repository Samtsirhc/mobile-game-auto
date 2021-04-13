
import base64
import json
# 防止https证书校验不正确
import ssl
import sys
import time
from urllib.error import URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen

ssl._create_default_https_context = ssl._create_unverified_context

API_KEY = 'j2oUYlGcF33SaXd12pEbRnO8'

SECRET_KEY = 'aMFVEcpiSsnUYY0spPuzTRd1XjKBqK8g'

OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"  # https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic 高精度

TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    result_str = result_str.decode()

    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

def request(url, data):
    req = Request(url, data.encode('utf-8'))
    try:
        f = urlopen(req)
        result_str = f.read()
        result_str = result_str.decode()
        return result_str
    except URLError as err:
        print(err)


def re(image_url, img):
    result = request(image_url, urlencode({'image': base64.b64encode(img)}))
    result_json = json.loads(result)
    # print(result_json)
    if 'error_code' in result_json:
        time.sleep(0.5)
        return re(image_url, img)
    else:
        for words_result in result_json["words_result"]:
            return words_result["words"]


def my_orc(img):
    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token

    # 解析返回结果
    text = re(image_url, img)
    time.sleep(1)
    return text


