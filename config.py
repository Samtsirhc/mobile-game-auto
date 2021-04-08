from tools.logger import creat_my_logger, Logger
from tools.time_tool import *
from tools.path_tool import *
import requests
import string


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
    l = get_logger()
    l.info('4564')