import logging
import os
import sys
import time

import psutil

from config import APP_NAME, IMG_PATH, get_logger
from emulator import Emulator

logger = get_logger()


class check():
    def __init__(self, emulator: Emulator):
        self.emulator = emulator

    @staticmethod
    def 在主页(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        return emulator.find_img(f'{IMG_PATH}check\\{img_name}')

    @staticmethod
    def 在基建(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        return emulator.find_img(f'{IMG_PATH}check\\{img_name}')

    @staticmethod
    def 在进驻总览(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        return emulator.find_img(f'{IMG_PATH}check\\{img_name}')

    @staticmethod
    def 在换班(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        return emulator.find_img(f'{IMG_PATH}check\\{img_name}')


def 登录方舟(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    emulator.kill_app(APP_NAME)
    time.sleep(1)
    emulator.run_app(APP_NAME)
    time.sleep(30)
    emulator.kill_app(APP_NAME)
    time.sleep(1)
    emulator.run_app(APP_NAME)
    while True:
        time.sleep(1)
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\下载资源确认')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\start')
        if emulator.find_img(f'{IMG_PATH + dir_name}\\鹰角图标'):
            break
    while True:
        time.sleep(1)
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\账号管理')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\账号登录')
        if emulator.find_img(f'{IMG_PATH + dir_name}\\输入密码'):
            break
    while True:
        if not emulator.find_img(f'{IMG_PATH + dir_name}\\确认密码'):
            emulator.find_and_click(f'{IMG_PATH + dir_name}\\输入密码')
            time.sleep(1)
        else:
            if not emulator.find_img(f'{IMG_PATH + dir_name}\\已输入密码'):
                emulator.input_text('1qaz741.')
            else:
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\确认密码')
                break
    while True:
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\登录')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\活动X')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\月卡收货', (0, 200))
        # emulator.find_and_click(f'{IMG_PATH + dir_name}\\签到X')
        if check.在主页(emulator):
            logger.info(dir_name)
            break
    pass


def 进入基建(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        if check.在基建(emulator):
            break
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\基建')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\导航小房子')
        time.sleep(1)
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\导航基建')
        time.sleep(1)
    pass


def 基建换班(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\进驻总览')
        if check.在进驻总览(emulator):
            break
    dorm_order = 0
    switch_state = 0    # 换班状态，0：在找宿舍；1：在换干员
    switch_step = 0
    while True:
        # 找宿舍
        if dorm_order < 3 and switch_state == 0:
            emulator.swipe((1216, 650, 1215, 158))
            time.sleep(1)
            emulator.find_and_click(f'{IMG_PATH + dir_name}\\宿舍', (236, 51))
            if check.在换班(emulator):
                switch_state = 1
                dorm_order += 1
                pass

        # 安排干员休息
        if switch_state == 1:
            if switch_step < 3:
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\清空选择')
                switch_step += 1
            if switch_step == 3:
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\心情上')
                if emulator.find_img(f'{IMG_PATH + dir_name}\\心情下'):
                    switch_step += 1
            if switch_step == 4:
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\心情下')
                if emulator.find_img(f'{IMG_PATH + dir_name}\\心情上'):
                    switch_step += 1
            if switch_step == 5:
                for wife_x in range(5):
                    for wife_y in range(2):
                        emulator.click(
                            (487 + wife_x * 145, 226 + wife_y * 250))
                        time.sleep(0.7)
                switch_step += 1
            if switch_step == 6:
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\确认')
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\红底白勾')
                if check.在进驻总览(emulator):
                    switch_step = 0
                    switch_state = 0

        # 干员上班
        if dorm_order > 2 and switch_state == 0:
            if switch_step == 0:
                emulator.find_and_click(
                    f'{IMG_PATH + dir_name}\\干员空位', (10, 28))
                if check.在换班(emulator) or emulator.find_img(f'{IMG_PATH + dir_name}\\单人上班'):
                    switch_step += 1

            if switch_step == 1:
                for wife_x in range(5):
                    for wife_y in range(2):
                        emulator.click(
                            (487 + wife_x * 145, 226 + wife_y * 250))
                        time.sleep(0.7)
                switch_step += 1

            if switch_step == 2:
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\确认')
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\红底白勾')
                if check.在进驻总览(emulator):
                    switch_step = 0

            if not emulator.find_img(f'{IMG_PATH + dir_name}\\干员空位'):
                if emulator.find_img(f'{IMG_PATH + dir_name}\\控制中枢'):
                    break
                if check.在进驻总览(emulator):
                    emulator.swipe((1216, 158, 1215, 550))
                    time.sleep(1)
    logger.info(dir_name)
    pass


def 基建收菜(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\白色铃铛')
        if emulator.find_img(f'{IMG_PATH + dir_name}\\蓝色铃铛'):
            for _ in range(7):
                emulator.find_and_click(
                    f'{IMG_PATH + dir_name}\\待办事项', (180, 0))
                time.sleep(0.5)
            emulator.find_and_click(f'{IMG_PATH + dir_name}\\蓝色铃铛')
            break
    logger.info(dir_name)
    pass


def 使用无人机(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\贸易站1')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\贸易站2')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\贸易站3')
        if emulator.find_img(f'{IMG_PATH + dir_name}\\获取中'):
            break
    while True:
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\获取中', (-344, 0))
        if emulator.find_img(f'{IMG_PATH + dir_name}\\无人机协助'):
            break

    trade_step = 0
    while True:
        while trade_step == 0:
            if emulator.find_and_click(f'{IMG_PATH + dir_name}\\无人机协助'):
                trade_step += 1
        while trade_step > 0 and trade_step < 10:
            if emulator.find_and_click(f'{IMG_PATH + dir_name}\\最多'):
                trade_step += 4
        while trade_step > 10 and trade_step < 20:
            time.sleep(0.5)
            emulator.find_and_click(f'{IMG_PATH + dir_name}\\最多', (0, 260))
            trade_step += 4
        while trade_step > 20 and trade_step < 30:
            time.sleep(1)
            if emulator.find_img(f'{IMG_PATH + dir_name}\\无人机用完了'):
                trade_step += 100
            elif emulator.find_img(f'{IMG_PATH + dir_name}\\无人机协助'):
                emulator.find_and_click(f'{IMG_PATH + dir_name}\\可交付')
                time.sleep(1)
                trade_step = 0
        if trade_step > 100:
            break
    logger.info(dir_name)


def 去战斗(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        if emulator.find_img(f'{IMG_PATH + dir_name}\\在战斗页面'):
            break
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\导航小房子')
        time.sleep(1)
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\作战')
    pass


def 刷经验(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        if emulator.find_img(f'{IMG_PATH + dir_name}\\关卡已选择'):
            break
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\物资筹备')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\战术演习')
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\LS-5')
    pass


def 循环挑战(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        if emulator.find_img(f'{IMG_PATH + dir_name}\\战斗中'):
            time.sleep(30)
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\未代理', (50, 20))
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\已代理', (50, 70))
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\战斗完成', (0, -200))
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\开始行动')
        if emulator.find_img(f'{IMG_PATH + dir_name}\\体力刷完了'):
            break
    for _ in range(3):
        time.sleep(1)
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\体力刷完了')
    logger.info(dir_name)
    pass


def 去首页(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    while True:
        if emulator.find_img(f'{IMG_PATH + dir_name}\\在首页'):
            break
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\导航小房子')
        time.sleep(1)
        emulator.find_and_click(f'{IMG_PATH + dir_name}\\导航小房子', (-146, 156))
    pass


def 信用点(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    credit_step = 0
    while credit_step == 0:
        if emulator.find_and_click(f'{IMG_PATH + dir_name}\\采购中心'):
            credit_step += 1
    while credit_step == 1:
        if emulator.find_and_click(f'{IMG_PATH + dir_name}\\信用交易所'):
            credit_step += 1
    while credit_step == 2:
        if emulator.find_and_click(f'{IMG_PATH + dir_name}\\在交易所'):
            credit_step += 1
    while credit_step == 3:
        if emulator.find_and_click(f'{IMG_PATH + dir_name}\\已领取'):
            credit_step += 1
        if emulator.find_and_click(f'{IMG_PATH + dir_name}\\收取信用'):
            emulator.click((1122, 109))
            credit_step += 1
    if credit_step == 4:
        time.sleep(1)
        emulator.click((1122, 109))
        for items in range(5):
            time.sleep(1)
            emulator.click((131 + items*245, 267))
            getting = True
            while getting:
                time.sleep(0.5)
                if emulator.find_img(f'{IMG_PATH + dir_name}\\信用不足'):
                    getting = False
                    break
                if not emulator.find_and_click(f'{IMG_PATH + dir_name}\\购买物品'):
                    emulator.click((1122, 109))
                    getting = False
    logger.info(dir_name)
    pass


def 收日常任务(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    task_step = 0
    while task_step == 0:
        if emulator.find_and_click(f'{IMG_PATH + dir_name}\\任务'):
            task_step += 1
    if task_step == 1:
        for _ in range(90):
            emulator.click((1122, 140))
            time.sleep(0.5)
    logger.info(dir_name)
