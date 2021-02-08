from tools.logger import creat_my_logger, Logger
from tools.time_tool import *


PCR_IMG_PATH = ".\\imgs\\pcr\\"
PCR_APP_NAME = "com.netease.uu"
LOG_PATH = ".\\logs\\"
LOG_NAME = ''

def get_logger(log_file_name=PCR_LOG_NAME):
    logger = Logger(log_path=LOG_PATH, log_file_name = log_file_name)
    logger = logger.get_logger()
    return logger

def check_job(checker):
    log_name = f'{get_time(4)}.log'
    log_path = f'{LOG_PATH}{log_name}'
    log_content = ''
    with open(log_path, 'r') as f:
        log_content += f.read()
        if checker in log_content:
            return True
        else:
            return False
