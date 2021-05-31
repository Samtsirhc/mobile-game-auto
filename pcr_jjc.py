import requests
import json

jjc_url = r"https://api.pcrdfans.com/x/v1/search"


payload = {"_sign":"切噜~蹦蹦铃切铃铃铃噼啪蹦噜唎啪唎噼噜唎蹦唎切噼蹦蹦唎铃唎哔哔切","def":[105201,103401,101001,100201,101801],"language":0,"nonce":"3bal4k70zvtzb28a","page":1,"region":3,"sort":1,"ts":1622430684}

re = requests.post(jjc_url, data=json.dumps(payload))
re = re.text
print(re)
# def AnalysisJJCData(response):
#     if type(response) != str:
#         print("错了")
#         return None
#     if response['code'] != 0:
#         print("错了")
#         return None
#     result = response['data']
#     print(result)
#     pass

# if __name__ == "__main__":
#     AnalysisJJCData(re)
#     pass