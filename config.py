from tools.logger import creat_my_logger, Logger
from tools.time_tool import *
from tools.path_tool import *
import requests
import string
import json
import os


# basic settings
ABS_PATH = get_path()
EMULATOR_PATH = "C:\\Users\\lcyba\\Desktop\\夜神模拟器.lnk"

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


class Periodic():
    def __init__(self, log_list, name, loop_type):
        '''
        log_list：循环的任务列表
        name：任务组的名称
        loop_type：循环的类型。1，日循环；7，周循环
        '''
        self.name = name
        self.init_basic_log(log_list)
        self.set_loop_type(loop_type)
        self.check_log()
        
    def init_basic_log(self, log_list):
        self.basic_log = {}
        for i in log_list:
            self.basic_log[i] = False
        self.basic_log = json.dumps(self.basic_log, ensure_ascii=False)

    def check_log(self):
        if os.path.isfile(self.log_path):
            with open(self.log_path, 'rb') as f:
                self.log = json.load(f)
            pass
        else:
            with open(self.log_path, 'w', encoding = 'utf-8') as f:
                f.write(self.basic_log)
            with open(self.log_path, 'rb') as f:
                self.log = json.load(f)

    def set_loop_type(self, loop_type):
        self.week = get_week()
        self.date = get_time(4)
        if loop_type == 1:
            self.log_path = f'{LOG_PATH}{self.name} {self.date}.json'
        elif loop_type == 7:
            self.log_path = f'{LOG_PATH}{self.name} {self.week}.json'
        else:
            print('error!!!!!!!!!!!!')
    
    def check(self, key):
        return self.log[key]

    def finish(self, key):
        with open(self.log_path, 'rb') as f:
            self.log = json.load(f)
            self.log[key] = True
        with open(self.log_path, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(self.log, ensure_ascii=False))

    def periodic_manager(self, func):
        def dec():
            if self.check(func.__name__):
                pass
            else:
                func()
        return dec


def get_logger():
    logger = Logger(log_path=LOG_PATH, log_file_name = LOG_NAME, cq_config = CQHTTP_CONFIG)
    logger = logger.get_logger()
    return logger

if __name__ == '__main__' :
    pass