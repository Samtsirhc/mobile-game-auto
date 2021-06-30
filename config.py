from modules.logger import creat_my_logger, Logger
import json
import os
# import pcr_data


def get_logger():
    CQHTTP_CONFIG = "http://127.0.0.1:5700/send_private_msg?user_id=812266890&message=MSG"
    logger = Logger(log_path='logs/', log_file_name = '', cq_config = CQHTTP_CONFIG)
    logger = logger.get_logger()
    return logger

if __name__ == '__main__' :
    # print(pcr_data.unit.UNIT_DATA)
    pass