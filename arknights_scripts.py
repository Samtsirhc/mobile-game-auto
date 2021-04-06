import logging
import os
import sys
import time

import psutil

from config import *
from emulator import Emulator


logger = get_logger()
emulator = Emulator(ARKNIGHTS_IMG_PATH)
# dir_name = sys._getframe().f_code.co_name
# path = f'{ARKNIGHTS_IMG_PATH + dir_name}\\'

@emulator.dir_decorator
def 登录方舟():
    emulator.run_app(ARKNIGHTS_APP_NAME)
    time.sleep(10)
    while not emulator.find_img(f'鹰角图标'):
        emulator.find_and_click(['下载资源确认','start'])
    while not emulator.find_img(f'输入密码'):
        emulator.find_and_click(['账号管理','账号登录'])
    while True:
        if not emulator.find_img(f'确认密码'):
            emulator.find_and_click(f'输入密码')
        else:
            if not emulator.find_img(f'已输入密码'):
                emulator.input_text('1qaz741.')
            else:
                emulator.find_and_click(f'确认密码')
                break
    _tmp = 0
    while _tmp < 2 :
        emulator.find_and_click(['登录','活动X','月卡收货'],[(0,0),(0,0),(0,200)])
        if emulator.find_img(f'在主页'):
            _tmp += 1

@emulator.dir_decorator
def 进入基建():
    while not emulator.find_img('在基建'):
        emulator.find_and_click(['导航基建','基建','导航小房子'])
        time.sleep(1)
    pass

@emulator.dir_decorator
def 基建换班():
    进入基建()
    while True:
        emulator.find_and_click(f'进驻总览')
        if emulator.find_img(f'在进驻总览'):
            break

    dorm_order = 1
    while dorm_order < 5:
        emulator.swipe((1216, 650, 1215, 300))
        time.sleep(1)
        if dorm_order < 4:
            emulator.find_and_click('宿舍')
            if emulator.find_img(f'宿舍{dorm_order}'):
                emulator.find_and_click(f'宿舍', (236, 51))
        elif emulator.find_and_click('B4宿舍',(98,87)):
            if emulator.find_img(f'宿舍{dorm_order}'):
                emulator.find_and_click(f'B4宿舍', (236, 130))

        # 宿舍换班    
        if emulator.find_img('在换班'):
            switch_step = 0
            while switch_step < 10:
                if switch_step < 3:
                    emulator.find_and_click(f'清空选择')
                    switch_step += 1
                if switch_step == 3:
                    for _ in range(3):
                        time.sleep(0.1)
                        emulator.click((1053, 47))
                    switch_step += 1
                    time.sleep(1)
                if switch_step == 4:
                    if emulator.find_img('心情上'):
                        switch_step += 1
                    else:
                        emulator.click((1053, 47))
                        time.sleep(0.5)
                if switch_step == 5:
                    for wife_x in range(5):
                        for wife_y in range(2):
                            emulator.click(
                                (487 + wife_x * 145, 226 + wife_y * 250))
                            time.sleep(0.1)
                    switch_step += 1
                if switch_step == 6:
                    emulator.find_and_click(['确认','红底白勾'])
                    if emulator.find_img(f'在进驻总览'):
                        switch_step = 99
                        dorm_order += 1

    switch_step = 0
    while True:
        if switch_step == 0:
            emulator.find_and_click('干员空位', (10, 28))
            if emulator.find_img(f'在换班'):
                switch_step += 1

        if switch_step == 1:
            for wife_x in range(3):
                for wife_y in range(2):
                    emulator.click((487 + wife_x * 145, 226 + wife_y * 250))
                    time.sleep(0.7)
            switch_step += 1

        if switch_step == 2:
            emulator.find_and_click(['确认','红底白勾'])
            if emulator.find_img(f'在进驻总览'):
                switch_step = 0

        if not emulator.find_img(f'干员空位'):
            if emulator.find_img(f'控制中枢'):
                break
            if emulator.find_img(f'在进驻总览'):
                emulator.swipe((1216, 158, 1215, 450))
                time.sleep(1)

@emulator.dir_decorator
def 基建收菜():
    进入基建()
    while True:
        emulator.find_and_click(f'白色铃铛')
        if emulator.find_img(f'蓝色铃铛'):
            for _ in range(7):
                emulator.find_and_click('待办事项', (180, 0))
                time.sleep(0.5)
            emulator.find_and_click('蓝色铃铛')
            break
    while True:
        if emulator.find_img('制造站'):
            break
        else:
            emulator.click((364,320))
    _tmp = 0
    while True:
        emulator.find_and_click(['制造中', '最多', '勾'])
        if emulator.find_and_click('最多'):
            _tmp += 1
        if _tmp > 4:
            break
    for _ in range(5):
        emulator.click((60,40))
        time.sleep(0.5)
    pass 

@emulator.dir_decorator
def 使用无人机():
    进入基建()
    while True:
        emulator.find_and_click(['贸易站1', '贸易站2', '贸易站3'])
        if emulator.find_img(f'获取中'):
            break
    while True:
        emulator.find_and_click(f'获取中', (-344, 0))
        if emulator.find_img(f'无人机协助'):
            break

    while True:
        if emulator.find_img(f'无人机用完了'):
            break
        emulator.find_and_click(['可交付', '无人机协助'])
        if emulator.find_img(f'确定'):
            emulator.click((959, 338))
            emulator.click((959, 338))
            emulator.find_and_click('确定')

@emulator.dir_decorator
def 去战斗():
    while True:
        if emulator.find_img(f'在战斗页面'):
            break
        emulator.find_and_click(['作战','导航小房子'])
        time.sleep(1)
    pass

@emulator.dir_decorator
def 选择关卡():
    while True:
        if emulator.find_img(f'关卡已选择'):
            break
        emulator.find_and_click(['物资筹备','战术演习','LS-5'])
        # emulator.find_and_click(["源石尘行动","行动记录","OD-6"])
        # emulator.find_and_click(['画中人','入画','WR-3'])
    pass

@emulator.dir_decorator
def 循环挑战():
    while not emulator.find_img(f'体力刷完了'):
        if emulator.find_img(f'战斗中'):
            time.sleep(30)
        emulator.find_and_click(['未代理','已代理','战斗完成','开始行动'], [(50, 20),(50, 70),(0, -200),(0,0)])
    for _ in range(3):
        time.sleep(1)
        emulator.find_and_click(f'体力刷完了')
    pass

@emulator.dir_decorator
def 去首页():
    while not emulator.find_img(f'在首页'):
        emulator.find_and_click(f'导航小房子')
        time.sleep(1)
        emulator.find_and_click(f'导航小房子', (-146, 156))
    pass

@emulator.dir_decorator
def 信用点():
    credit_step = 0
    while credit_step == 0:
        if emulator.find_and_click(f'采购中心'):
            credit_step += 1
    while credit_step == 1:
        if emulator.find_and_click(f'信用交易所'):
            credit_step += 1
    while credit_step == 2:
        if emulator.find_and_click(f'在交易所'):
            credit_step += 1
    while credit_step == 3:
        if emulator.find_and_click(f'已领取'):
            credit_step += 1
        if emulator.find_and_click(f'收取信用'):
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
                if emulator.find_img(f'信用不足'):
                    getting = False
                    break
                if not emulator.find_and_click(f'购买物品'):
                    emulator.click((1122, 109))
                    getting = False
    pass

@emulator.dir_decorator
def 刷土():
    去战斗()
    tmp = 0
    while tmp == 0:
        emulator.swipe((100,300,500,300))
        time.sleep(1)
        if emulator.find_and_click('黑暗时代下'):
            tmp += 1
    
    while tmp == 1:
        emulator.find_and_click('1-7')
        if emulator.find_img(f'关卡已选择'):
            break
    pass

@emulator.dir_decorator
def 收日常任务():
    task_step = 0
    while task_step == 0:
        if emulator.find_and_click(f'任务'):
            task_step += 1
    if task_step == 1:
        for _ in range(90):
            emulator.click((1122, 140))
            time.sleep(0.5)

if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)

    # 登录方舟()
    # 基建换班()
    # 基建收菜()
    # 使用无人机()
    刷土()
    循环挑战()
    信用点()
    收日常任务()

