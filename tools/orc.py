
import base64
import json
# 防止https证书校验不正确
import ssl
import sys
import time
from urllib.error import URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen



class Orc:
    def __init__(self):
        
        self.API_KEY = 'j2oUYlGcF33SaXd12pEbRnO8'
        self.SECRET_KEY = 'aMFVEcpiSsnUYY0spPuzTRd1XjKBqK8g'
        self.OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"  # https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic 高精度
        self.TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
        self.token = self.fetch_token()
        self.image_url = self.OCR_URL + "?access_token=" + self.token


    def fetch_token(self):
        ssl._create_default_https_context = ssl._create_unverified_context
        params = {'grant_type': 'client_credentials',
                'client_id': self.API_KEY,
                'client_secret': self.SECRET_KEY}
        post_data = urlencode(params)
        post_data = post_data.encode('utf-8')
        req = Request(self.TOKEN_URL, post_data)
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


    def request(self, url, data):
        req = Request(url, data.encode('utf-8'))
        try:
            f = urlopen(req)
            result_str = f.read()
            result_str = result_str.decode()
            return result_str
        except URLError as err:
            print(err)


    def recognize(self, img):
        '''
        '''
        result = self.request(self.image_url, urlencode({'image': base64.b64encode(img)}))
        result_json = json.loads(result)
        # print(result_json)
        if 'error_code' in result_json:
            time.sleep(0.5)
            return self.recognize(img)
        else:
            for words_result in result_json["words_result"]:
                return words_result["words"]

if __name__ == "__main__":
    orcer = Orc()
    with open('1.jpg', 'rb') as f:
        a = f.read()
        b = orcer.recognize(a)
        print(b)
