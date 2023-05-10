import logging
import os
import sys
import time
from cv2 import cv2
import random
from config import get_logger
from emulator import Emulator
from modules.periodic import Periodic
from modules.tools import load_img
from modules.process_tool import close_process

img_path = 'imgs/daily/'
emulator = Emulator(img_path)
APP_NAME = "com.mihoyo.hyperion"
logger = get_logger()

@emulator.dir_decorator
def 原神签到():
    emulator.connect(0)
    emulator.kill_app(APP_NAME)
    emulator.run_app(APP_NAME)
    _is_app_ready = False
    while not _is_app_ready:
        _is_app_ready = emulator.check_app(APP_NAME)
        time.sleep(3)

    # 米游社签到
    _app_check_out = False
    _app_check_out_start_time = time.time()
    _app_check_out_duration = 0
    while not _app_check_out:
        _app_check_out_duration = time.time() - _app_check_out_start_time
        if _app_check_out_duration > 60:
            _app_check_out = True
        emulator.find_and_click(['米游社签到'])
        if emulator.find_img('米游社签到完成'):
            _app_check_out = True
        time.sleep(1)
    
    # 原神签到
    _yuanshen_check_out = False
    _yuanshen_check_out_start_time = time.time()
    _yuanshen_check_out_duration = 0
    while not _yuanshen_check_out:
        _yuanshen_check_out_duration = time.time() - _yuanshen_check_out_start_time
        if _yuanshen_check_out_duration > 60:
            _yuanshen_check_out = True
        emulator.find_and_click(['领取', '打开原神签到'])
        if emulator.find_img('签到成功'):
            _yuanshen_check_out = True
        time.sleep(1)
    


@emulator.dir_decorator
def 崩铁签到():
    emulator.connect(2)
    emulator.kill_app(APP_NAME)
    emulator.run_app(APP_NAME)
    _is_app_ready = False
    while not _is_app_ready:
        _is_app_ready = emulator.check_app(APP_NAME)
        time.sleep(3)

    # 米游社签到
    _app_check_out = False
    _app_check_out_start_time = time.time()
    _app_check_out_duration = 0
    while not _app_check_out:
        _app_check_out_duration = time.time() - _app_check_out_start_time
        if _app_check_out_duration > 60:
            _app_check_out = True
        emulator.find_and_click(['米游社签到'])
        if emulator.find_img('米游社签到完成'):
            _app_check_out = True
        time.sleep(1)
    
    # 崩铁签到
    _yuanshen_check_out = False
    _yuanshen_check_out_start_time = time.time()
    _yuanshen_check_out_duration = 0
    while not _yuanshen_check_out:
        _yuanshen_check_out_duration = time.time() - _yuanshen_check_out_start_time
        if _yuanshen_check_out_duration > 60:
            _yuanshen_check_out = True
        emulator.find_and_click(['领取2', '打开崩铁签到'])
        if emulator.find_img('签到成功2'):
            _yuanshen_check_out = True
        time.sleep(1) 


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    emulator.connect()
    签到()
