from tools.logger import creat_my_logger, Logger
from tools.time_tool import *
from tools.path_tool import *
import requests
import string
import json
import os


# basic settings
ABS_PATH = get_path()
EMULATOR_PATH = "C:\\Users\\licy03\\Desktop\\夜神模拟器.lnk"

PCR_IMG_PATH = ABS_PATH + "\\imgs\\pcr\\"
PCR_APP_NAME = "com.netease.uu"

ARKNIGHTS_IMG_PATH = ABS_PATH + "\\imgs\\arknights\\"
ARKNIGHTS_APP_NAME = "com.hypergryph.arknights"

LOG_PATH = ABS_PATH + "\\logs\\"
LOG_NAME = ''
CQHTTP_CONFIG = 'http://127.0.0.1:5700/send_private_msg?user_id=812266890&message=MSG'

# settings
MINING = True # 是否搓玉

# globle var
CURRENT_DIR = ''

class ArknightsWeekly():
    def __init__(self):
        self.week = get_week()
        self.basic_log = {'剿灭':False, '周任务': False}
        self.basic_log = json.dumps(self.basic_log)
        self.log_path = f'{LOG_PATH}{self.week}.json'
        self.chekc_log()

        pass

    def chekc_log(self):
        if os.path.isfile(self.log_path):
            with open(self.log_path, 'rb') as f:
                self.log = json.load(f)
                print(self.log)
            pass
        else:
            with open(self.log_path, 'w', encoding = 'utf-8') as f:
                f.write(self.basic_log)
    
    def finish_job(self, job_name):
        with open(self.log_path, 'rb') as f:
            self.log = json.load(f)
            self.log[job_name] = True
        with open(self.log_path, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(self.log))
    
    def check_job(self, job_name):
        return self.log[job_name]






def get_logger():
    logger = Logger(log_path=LOG_PATH, log_file_name = LOG_NAME, cq_config = CQHTTP_CONFIG)
    logger = logger.get_logger()
    return logger

def check_job(checker):
    '''
    检查关键字checker在不在日志里面
    '''
    log_name = f'{get_time(4)}.log'
    log_path = f'{LOG_PATH}{log_name}'
    log_content = ''
    with open(log_path, 'r') as f:
        log_content += f.read()
        if checker in log_content:
            return True
        else:
            return False

if __name__ == '__main__' :
    a = ArknightsWeekly()