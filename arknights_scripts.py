import logging
import os
import sys
import time

import psutil

from config import *
from emulator import Emulator

logger = get_logger()

# dir_name = sys._getframe().f_code.co_name
# path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'


class check():
    def __init__(self, emulator: Emulator):
        self.emulator = emulator

    @staticmethod
    def 在主页(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        path = f'{ARKNIGHTS_IMG_PATH}'
        return emulator.find_img(f'check\\{img_name}', path)

    @staticmethod
    def 在基建(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        path = f'{ARKNIGHTS_IMG_PATH}'
        return emulator.find_img(f'check\\{img_name}', path)

    @staticmethod
    def 在进驻总览(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        path = f'{ARKNIGHTS_IMG_PATH}'
        return emulator.find_img(f'check\\{img_name}', path)

    @staticmethod
    def 在换班(emulator: Emulator):
        img_name = sys._getframe().f_code.co_name
        path = f'{ARKNIGHTS_IMG_PATH}'
        return emulator.find_img(f'check\\{img_name}', path)


def 登录方舟(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    emulator.run_app(ARKNIGHTS_APP_NAME)
    _timer = 0
    while True:
        _timer += 1
        time.sleep(1)
        emulator.find_and_click(f'下载资源确认', path)
        emulator.find_and_click(f'start', path)
        if emulator.find_img(f'鹰角图标', path):
            break
        if _timer > 100:
            emulator.kill_app(ARKNIGHTS_APP_NAME)
            time.sleep(3)
            emulator.run_app(ARKNIGHTS_APP_NAME)
            _timer = 0
    while True:
        time.sleep(1)
        emulator.find_and_click(f'账号管理', path)
        emulator.find_and_click(f'账号登录', path)
        if emulator.find_img(f'输入密码', path):
            break
    while True:
        if not emulator.find_img(f'确认密码', path):
            emulator.find_and_click(f'输入密码', path)
            time.sleep(1)
        else:
            if not emulator.find_img(f'已输入密码', path):
                emulator.input_text('1qaz741.')
            else:
                emulator.find_and_click(f'确认密码', path)
                break
    while True:
        emulator.find_and_click(f'登录', path)
        emulator.find_and_click(f'活动X', path)
        emulator.find_and_click(f'月卡收货', path,  (0, 200))
        # emulator.find_and_click(f'签到X', path)
        if check.在主页(emulator):
            logger.info(dir_name)
            break
    pass


def 画中人(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        if emulator.find_img(f'关卡已选择', path):
            break
        emulator.find_and_click(f'画中人', path)
        emulator.find_and_click(f'入画', path)
        emulator.find_and_click(f'WR-3', path)
    pass


def 进入基建(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        if check.在基建(emulator):
            break
        emulator.find_and_click(f'基建', path)
        emulator.find_and_click(f'导航小房子', path)
        time.sleep(1)
        emulator.find_and_click(f'导航基建', path)
        time.sleep(1)
    pass


def 基建换班(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        emulator.find_and_click(f'进驻总览', path)
        if check.在进驻总览(emulator):
            break
    dorm_order = 0
    switch_state = 0    # 换班状态，0：在找宿舍；1：在换干员
    switch_step = 0
    while True:
        # 找宿舍
        if dorm_order < 4 and switch_state == 0:
            emulator.swipe((1216, 650, 1215, 158))
            time.sleep(1)
            emulator.find_and_click(f'宿舍', path, (236, 51))
            if check.在换班(emulator):
                switch_state = 1
                dorm_order += 1
                pass

        # 安排干员休息
        if switch_state == 1:
            if switch_step < 3:
                emulator.find_and_click(f'清空选择', path)
                switch_step += 1
            if switch_step == 3:
                emulator.find_and_click(f'心情上', path)
                if emulator.find_img(f'心情下', path):
                    switch_step += 1
            if switch_step == 4:
                emulator.find_and_click(f'心情下', path)
                if emulator.find_img(f'心情上', path):
                    switch_step += 1
            if switch_step == 5:
                for wife_x in range(5):
                    for wife_y in range(2):
                        emulator.click(
                            (487 + wife_x * 145, 226 + wife_y * 250))
                        time.sleep(0.1)
                switch_step += 1
            if switch_step == 6:
                emulator.find_and_click(['确认','红底白勾'], path)
                if check.在进驻总览(emulator):
                    switch_step = 0
                    switch_state = 0

        # 干员上班
        if dorm_order > 3 and switch_state == 0:
            if switch_step == 0:
                emulator.find_and_click(
                    f'干员空位', path, (10, 28))
                if check.在换班(emulator) or emulator.find_img(f'单人上班', path):
                    switch_step += 1

            if switch_step == 1:
                for wife_x in range(5):
                    for wife_y in range(2):
                        emulator.click(
                            (487 + wife_x * 145, 226 + wife_y * 250))
                        time.sleep(0.7)
                switch_step += 1

            if switch_step == 2:
                emulator.find_and_click(f'确认', path)
                emulator.find_and_click(f'红底白勾', path)
                if check.在进驻总览(emulator):
                    switch_step = 0

            if not emulator.find_img(f'干员空位', path):
                if emulator.find_img(f'控制中枢', path):
                    break
                if check.在进驻总览(emulator):
                    emulator.swipe((1216, 158, 1215, 550))
                    time.sleep(1)
    logger.info(dir_name)
    pass


def 基建收菜(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        emulator.find_and_click(f'白色铃铛', path)
        if emulator.find_img(f'蓝色铃铛', path):
            for _ in range(7):
                emulator.find_and_click(
                    f'待办事项', path, (180, 0))
                time.sleep(0.5)
            emulator.find_and_click(f'蓝色铃铛', path)
            break
    logger.info(dir_name)
    pass


def 使用无人机(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        emulator.find_and_click(['贸易站1', '贸易站2', '贸易站3'], path)
        if emulator.find_img(f'获取中', path):
            break
    while True:
        emulator.find_and_click(f'获取中', path, (-344, 0))
        if emulator.find_img(f'无人机协助', path):
            break

    while True:
        if emulator.find_img(f'无人机用完了', path):
            break
        emulator.find_and_click(['可交付', '无人机协助'], path)
        if emulator.find_img(f'确定', path):
            emulator.click((959, 338))
            emulator.click((959, 338))
            emulator.find_and_click('确定', path)
    logger.info(dir_name)


def 去战斗(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        if emulator.find_img(f'在战斗页面', path):
            break
        emulator.find_and_click(f'导航小房子', path)
        time.sleep(1)
        emulator.find_and_click(f'作战', path)
    pass


def 刷经验(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        if emulator.find_img(f'关卡已选择', path):
            break
        emulator.find_and_click(f'物资筹备', path)
        emulator.find_and_click(f'战术演习', path)
        emulator.find_and_click(f'LS-5', path)
    pass


def 循环挑战(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        if emulator.find_img(f'战斗中', path):
            time.sleep(30)
        emulator.find_and_click(f'未代理', path, (50, 20))
        emulator.find_and_click(f'已代理', path, (50, 70))
        emulator.find_and_click(f'战斗完成', path, (0, -200))
        emulator.find_and_click(f'开始行动', path)
        if emulator.find_img(f'体力刷完了', path):
            break
    for _ in range(3):
        time.sleep(1)
        emulator.find_and_click(f'体力刷完了', path)
    logger.info(dir_name)
    pass


def 去首页(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    while True:
        if emulator.find_img(f'在首页', path):
            break
        emulator.find_and_click(f'导航小房子', path)
        time.sleep(1)
        emulator.find_and_click(f'导航小房子', path, (-146, 156))
    pass


def 信用点(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    credit_step = 0
    while credit_step == 0:
        if emulator.find_and_click(f'采购中心', path):
            credit_step += 1
    while credit_step == 1:
        if emulator.find_and_click(f'信用交易所', path):
            credit_step += 1
    while credit_step == 2:
        if emulator.find_and_click(f'在交易所', path):
            credit_step += 1
    while credit_step == 3:
        if emulator.find_and_click(f'已领取', path):
            credit_step += 1
        if emulator.find_and_click(f'收取信用', path):
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
                if emulator.find_img(f'信用不足', path):
                    getting = False
                    break
                if not emulator.find_and_click(f'购买物品', path):
                    emulator.click((1122, 109))
                    getting = False
    logger.info(dir_name)
    pass


def 收日常任务(emulator: Emulator):
    dir_name = sys._getframe().f_code.co_name
    path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'
    task_step = 0
    while task_step == 0:
        if emulator.find_and_click(f'任务', path):
            task_step += 1
    if task_step == 1:
        for _ in range(90):
            emulator.click((1122, 140))
            time.sleep(0.5)
    logger.info(dir_name)


if __name__ == "__main__":
    emulator = Emulator()
    logger.setLevel(logging.DEBUG)
    基建换班(emulator)
