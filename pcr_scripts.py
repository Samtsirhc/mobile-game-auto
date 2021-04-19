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
log_list = ['MANA冒险', '经验值冒险', '地下城', '点赞', 'JJC', 'PJJC']
daily = Periodic(log_list, 'PCR', 1)

@emulator.dir_decorator
def 登录PCR():
    logger.info('开始登录PCR')
    emulator.run_app(PCR_APP_NAME)
    while not emulator.check_app('tw.sonet.princessconnect'):
        emulator.find_and_click(['我的', '加速'], [(-230, 10), (578, 37)])
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
            break


@emulator.dir_decorator
def 兰德索尔杯():
    for _ in range(3):
        time.sleep(1)
        emulator.click((266, 400))
    while True:
        if emulator.find_and_click('比赛开始'):
            return


@emulator.dir_decorator
def 去冒险():
    while True:
        emulator.find_and_click('冒险未激活')
        emulator.click((644, 655))
        time.sleep(0.5)
        if emulator.find_img('冒险已激活'):
            # 处于冒险页面
            break


@emulator.dir_decorator
def 去主页():
    while True:
        emulator.click((121, 655))
        time.sleep(0.5)
        if emulator.find_img('主页已激活'):
            # 处于主页
            break


@emulator.dir_decorator
def 扫荡():
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
        emulator.click((940, 442))
        if emulator.find_and_click('OK'):
            break
    while True:
        time.sleep(0.3)
        emulator.click((633, 640))
        emulator.click((893, 660))
        if emulator.find_img('扫荡完成'):
            break


@emulator.dir_decorator
def MANA冒险():
    if daily.check('MANA冒险'):
        return None
    去冒险()
    while True:
        emulator.find_and_click(['探索', '进入MANA冒险'])
        if emulator.find_img('在MANA冒险页面'):
            emulator.click((849, 198))
            time.sleep(2)
            if emulator.find_img('在扫荡页面'):
                break
    扫荡()
    daily.finish('MANA冒险')



@emulator.dir_decorator
def 经验值冒险():
    if daily.check('经验值冒险'):
        return None
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
    daily.finish('经验值冒险')


@emulator.dir_decorator
def 进入商店():
    去主页()
    while True:
        emulator.find_and_click('商店')
        if emulator.find_img('在商店'):
            break


@emulator.dir_decorator
def 买经验():
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


@emulator.dir_decorator
def 地下城():
    if daily.check('地下城'):
        return None
    去冒险()
    times = 3
    while True:
        emulator.find_and_click(['地下城', '蓝OK'])
        if emulator.find_and_click('EX3'):
            times -= 1
        if times < 0:
            break
        if emulator.find_img('返回'):
            break
    step = 1
    team = 1
    while True:
        if step == 1:
            time.sleep(1)
            emulator.find_and_click(['妈2', '妈', '进行挑战'])
            if emulator.find_img('EX3'):
                break
            if emulator.find_img('我的队伍'):
                step += 1
        if step == 2:
            time.sleep(1)
            emulator.find_and_click(['我的队伍', '地下城编组'])
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
            emulator.find_and_click(['下一步', 'OK', 'AUTO'])
            if emulator.find_and_click('前往地下城') and tmp:
                team += 1
                tmp = False
            if emulator.find_img('EX3'):
                break
            if emulator.find_img('返回'):
                time.sleep(3)
                if emulator.find_img('返回'):
                    step = 1
    daily.finish('地下城')


@emulator.dir_decorator
def 持续战斗():
    while True:
        time.sleep(3)
        emulator.find_and_click(['妈2', '妈', '进行挑战', '战斗开始', '下一步', '关闭', '取消'])


@emulator.dir_decorator
def 点赞():
    if daily.check('点赞'):
        return None
    去主页()
    _tmp = 0
    while True:
        emulator.find_and_click(['战队', '白底OK', 'OK', '成员情报'])
        if emulator.find_and_click(['赞', '无战队']):
            _tmp += 1
        if _tmp > 2:
            break
    daily.finish('点赞')


@emulator.dir_decorator
def 求装备():
    去主页()
    while True:
        emulator.find_and_click(['请求结果', 'OK', '战队', '白底OK', '装备请求', '请求'])
        if emulator.find_img(['请求状况', '无战队']):
            break

@emulator.dir_decorator
def JJC():
    if daily.check('JJC'):
        return None
    去冒险()
    state = 0
    while state == 0:
        if emulator.find_img('在竞技场'):
            state += 1
            break
        emulator.find_and_click('战斗竞技场')
    while state == 1:
        if not emulator.find_img('冷却完成'):
            time.sleep(10)
        else:
            emulator.find_and_click(['在竞技场','战斗开始'], [(10,10),(10,10)])
        if emulator.find_img('下一步'):
            state += 1
    while state == 2:
        emulator.find_and_click('下一步')
        if emulator.find_img('在竞技场'):
            break




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
