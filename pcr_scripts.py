import logging
import os
import sys
import time

from config import *
from emulator import Emulator
from tools.logger import creat_my_logger
from tools.time_tool import *

logger = get_logger()
emulator = Emulator(PCR_IMG_PATH)

@emulator.dir_decorator
def 登录PCR():
    logger.info('开始登录PCR')
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    emulator.run_app(PCR_APP_NAME)
    while not emulator.check_app('tw.sonet.princessconnect'):
        emulator.find_and_click(['我的','加速'], [(-230, 10), (578,37)])
    while not emulator.find_img('商店'):
        time.sleep(1)
        emulator.find_and_click('下载')
        emulator.click((650, 620))
        if emulator.find_img('请选择角色'):
            兰德索尔杯()
    while True:
        time.sleep(1)
        emulator.click((650, 620))
        if emulator.find_img('商店'):
            # 登录成功
            logger.info(dir_name)
            break

def 兰德索尔杯():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    for _ in range(3):
        time.sleep(1)
        emulator.click((266, 400))
    while True:
        if emulator.find_and_click('比赛开始'):
            return
    

def 去冒险():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    while True:
        emulator.find_and_click('冒险未激活')
        emulator.click((644, 655))
        time.sleep(0.5)
        if emulator.find_img('冒险已激活'):
            # 处于冒险页面
            break


def 去主页():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    while True:
        emulator.click((121, 655))
        time.sleep(0.5)
        if emulator.find_img('主页已激活'):
            # 处于主页
            break


def 扫荡():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    while True:
        if emulator.find_img('在扫荡页面'):
            break
    sweep_times = 5
    while sweep_times > 0:
        time.sleep(0.3)
        emulator.click((1179, 439))
        sweep_times -= 1
    while True:
        time.sleep(0.3)
        emulator.click((940,442))
        if emulator.find_and_click('OK'):
            break
    while True:
        time.sleep(0.3)
        emulator.click((633, 640))
        emulator.click((893, 660))
        if emulator.find_img('扫荡完成'):
            break


def MANA冒险():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    if check_job(dir_name):
        logger.info(dir_name)
        return True
    去冒险()
    while True:
        emulator.find_and_click('探索')
        emulator.find_and_click('MANA冒险')
        if emulator.find_img('在MANA冒险页面'):
            emulator.click((849, 198))
            time.sleep(2)
            if emulator.find_img('在扫荡页面'):
                break
    扫荡()
    logger.info(dir_name)


def 经验值冒险():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    if check_job(dir_name):
        logger.info(dir_name)
        return True
    去冒险()
    while True:
        emulator.find_and_click('探索')
        emulator.find_and_click('经验值冒险')
        if emulator.find_img('在经验值冒险页面'):
            emulator.click((849, 198))
            time.sleep(2)
            if emulator.find_img('在扫荡页面'):
                break
    扫荡()
    logger.info(dir_name)

def 进入商店():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    去主页()
    while True:
        emulator.find_and_click('商店')
        if emulator.find_img('在商店'):
            break


def 买经验():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    进入商店()
    if emulator.find_img('经验买完了'):
        return
    buy_times = 4
    while buy_times > 0:
        if emulator.find_and_click('选择'):
            buy_times -= 1
    while True:
        emulator.find_and_click('购买')
        emulator.find_and_click('OK')
        emulator.click((638, 614))
        if emulator.find_img('经验买完了'):
            return


def 地下城():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    if check_job(dir_name):
        logger.info(dir_name)
        return True
    去冒险()
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    times = 3
    while True:
        emulator.find_and_click(['地下城', '蓝OK'])
        if emulator.find_and_click('EX3'):
            times -= 1
        if times < 0:
            logger.info(dir_name)
            break
        if emulator.find_img('返回'):
            break
    step = 1
    team = 1
    while True:
        if step == 1:
            time.sleep(1)
            emulator.find_and_click(['妈2','妈','进行挑战'])
            if emulator.find_img('EX3'):
                logger.info(dir_name)
                break
            if emulator.find_img('我的队伍'):
                step += 1
        if step == 2:
            time.sleep(1)
            emulator.find_and_click(['我的队伍','地下城编组'])
            if emulator.find_img('在地下城编组'):
                step += 1
        if step == 3:
            if emulator.find_img('在地下城编组'):
                if team == 1:
                    emulator.click((1058, 273))
                if team == 2:
                    emulator.click((1058, 437))
                if team == 3:
                    emulator.click((1058, 568))
            if emulator.find_and_click('战斗开始'):
                step += 1
        tmp = True
        if step == 4:
            emulator.find_and_click(['下一步','OK','AUTO'])
            if emulator.find_and_click('前往地下城') and tmp:
                team += 1
                tmp = False
            if emulator.find_img('EX3'):
                logger.info(dir_name)
                break
            if emulator.find_img('返回'):
                time.sleep(3)
                if emulator.find_img('返回'):
                     step = 1 

def 持续战斗():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    while True:
        time.sleep(3)
        emulator.find_and_click(['妈2','妈','进行挑战','战斗开始','下一步','关闭','取消'])


def 点赞():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    if check_job(dir_name):
        logger.info(dir_name)
        return True
    去主页()
    _tmp = 0
    while True:
        emulator.find_and_click(['战队', '白底OK', 'OK', '成员情报'])
        if emulator.find_and_click(['赞','无战队']):
            _tmp += 1
        if _tmp > 4:
            break
    logger.info(dir_name)

def 求装备():
    dir_name = sys._getframe().f_code.co_name
    emulator.current_dir = dir_name
    去主页()
    while True:
        emulator.find_and_click(['请求结果', 'OK', '战队', '白底OK', '装备请求', '请求'])
        if emulator.find_img(['请求状况','无战队']):
            break
    logger.info(dir_name)

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    emulator.connect()
    登录PCR()
    地下城()
    MANA冒险()
    经验值冒险()
    点赞()
    求装备()
    pass
