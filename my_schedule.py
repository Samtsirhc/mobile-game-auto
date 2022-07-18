from modules.tools import load_json, write_json
import schedule
import requests
import time

ArkSettings = load_json("./config/Arknights.json")
ARK_COMMAND = '方舟 日常刷活动'
PCR_COMMMAND = 'pcr 日常'

url = "http://127.0.0.1:8888/"

def send_command(command):
    _res = requests.post(url, data = str(command).encode())

schedule.every().day.at("05:30").do(send_command,(ARK_COMMAND))
schedule.every().day.at("14:20").do(send_command,(PCR_COMMMAND)) 
schedule.every().day.at("12:30").do(send_command,(ARK_COMMAND))
# schedule.every().day.at("18:30").do(send_command,(PCR_COMMMAND)) 
schedule.every().day.at("22:30").do(send_command,(ARK_COMMAND))

if __name__ == "__main__":
    print("==========开始执行每日任务==========")
    while True:
        schedule.run_pending()
        time.sleep(30)
    

