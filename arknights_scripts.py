# !/usr/bin/python
# coding:utf-8

import logging
import os
import time

from emulator import Emulator
from modules.periodic import Periodic

log_list = ["剿灭", "周任务"]
weekly = Periodic(log_list, 'Arknights', 7, 'logs/')

emulator = Emulator("imgs/arknights/")
START_APP_NAME = "com.hypergryph.arknights"

@emulator.dir_decorator
def 登录方舟():
    emulator.run_app(START_APP_NAME)
    time.sleep(10)
    while not emulator.find_img(f'鹰角图标'):
        emulator.find_and_click(['下载资源确认', 'start'])
    while not emulator.find_img(f'输入密码'):
        emulator.find_and_click(['账号管理', '账号登录'])
    while True:
        if not emulator.find_img(f'确认密码'):
            emulator.find_and_click(f'输入密码')
            time.sleep(1)
        else:
            if not emulator.find_img(f'已输入密码'):
                emulator.input_text('1qaz741.')
            else:
                emulator.find_and_click(f'确认密码')
                break
    _tmp = 0
    while _tmp < 2:
        emulator.find_and_click(['登录', '活动X', '月卡收货'], [
            (0, 0), (0, 0), (0, 200)])
        if emulator.find_img(f'在主页'):
            _tmp += 1


def 结束():
    emulator.kill_app(START_APP_NAME)


@emulator.dir_decorator
def 进入基建():
    while not emulator.find_img('在基建'):
        if emulator.find_img('在导航'):
            emulator.find_and_click(['导航基建', '基建'])
        elif emulator.find_img('设施信息'):
            emulator.find_and_click('后退')
        else:
            emulator.find_and_click(['导航小房子', '基建'])
        time.sleep(1.5)
    pass


@emulator.dir_decorator
def 基建换班():
    facilities = {'宿舍': {'pos': [(794, 305), (794, 405), (794, 505), (794, 605)], 'count': 6},
                  '会客室': {'pos': [(1229, 212)], 'count': 3},
                  '控制中枢': {'pos': [(848, 158)], 'count': 6},
                  '制造站': {'pos': [(56, 315), (291, 315), (494, 315), (30, 412)], 'count': 4},
                  '贸易站': {'pos': [(167, 412), (381, 412)], 'count': 4},
                  '发电站': {'pos': [(72, 521), (277, 505), (477, 505)], 'count': 2},
                  '办公室': {'pos': [(1269, 410)], 'count': 2}}

    def 进驻信息换人(count):
        c_pos = [(482, 231), (482, 478), (630, 231),
                 (630, 478), (767, 231), (767, 478)]  # 角色的位置
        _tmp = 0
        while _tmp == 0:
            emulator.find_and_click(['进驻信息', '清空', '红底白勾'])
            if emulator.find_with('0人进驻', '进驻') == 2:
                _tmp += 1
        while _tmp == 1:
            emulator.find_and_click('进驻')
            if emulator.find_img('在换班'):
                _tmp += 1
        while _tmp == 2:
            for i in range(count):
                emulator.click(c_pos[i])
                time.sleep(0.2)
            _tmp += 1
        while _tmp == 3:
            emulator.find_and_click(['确认', '确认2'])
            if emulator.find_img(['进驻信息', '在进驻信息']):
                _tmp += 1

    def 进入设施(name, the_serial):
        # print(f'{name} {serial}')
        进入基建()
        _tmp = 0
        while _tmp == 0:
            if emulator.find_img([f'在{name}', '清空']):
                _tmp += 1
            else:
                emulator.click(facilities[name]['pos'][the_serial])
                time.sleep(3)

    for facility in facilities.keys():
        for serial in range(len(facilities[facility]['pos'])):
            进入设施(facility, serial)
            进驻信息换人(facilities[facility]['count'])


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
    去首页()
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
        time.sleep(1)
        if emulator.find_img(f'无人机用完了'):
            break
        else:
            emulator.find_and_click(['可交付', '无人机协助'])
            if emulator.find_img(f'确定'):
                emulator.click((959, 338))
                emulator.click((959, 338))
                emulator.click((956, 588))


@emulator.dir_decorator
def 去战斗():
    去首页()
    _tmp = [f'在战斗页面{i}' for i in range(1, 5)]
    while not emulator.find_img(_tmp):
        emulator.find_and_click('首页作战')
    pass


@emulator.dir_decorator
def 选择关卡():
    去战斗()
    while True:
        if emulator.find_img(["关卡已选择", "关卡已选择2"]):
            break
        # emulator.find_and_click(['物资筹备', '战术演习', 'LS-5'])
        # emulator.find_and_click(["源石尘行动","行动记录","OD-6"])
        # emulator.find_and_click(['画中人','入画','WR-3'])
        # emulator.find_and_click(["遗尘漫步", "漫漫独行", "WD-4"])
        # emulator.find_and_click(["覆潮之下", "荒败盐风", "SV-6"])
        # emulator.find_and_click(["灯火序曲", "路线安排", "PL-4"])
        emulator.find_and_click(["联锁竞赛", "始发营地", "FIN-TS"])
    pass


@emulator.dir_decorator
def 循环挑战():
    while not emulator.find_img(f'体力刷完了'):
        if emulator.find_img(f'战斗中'):
            time.sleep(30)
        emulator.find_and_click(['未代理', '已代理', '战斗完成', '开始行动'], [
            (50, 20), (50, 70), (0, -200), (0, 0)])
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
    去首页()
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
            emulator.click((131 + items * 245, 267))
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
    state = 0
    while state == 0:
        if emulator.find_img('左箭头'):
            state += 1
        emulator.find_and_click(['主线', '异卵同生', '觉醒'], [
            (0, 0), (-200, 0), (0, 0)])
    while state == 1:
        time.sleep(1.5)
        if not emulator.find_and_click('1-7'):
            emulator.swipe((800, 360, 400, 360))
        else:
            if emulator.find_img('关卡已选择'):
                state += 1

    pass


@emulator.dir_decorator
def 收日常任务():
    去首页()
    task_step = 0
    while task_step == 0:
        if emulator.find_and_click(f'任务'):
            task_step += 1
    if task_step == 1:
        for _ in range(90):
            emulator.click((1122, 140))
            time.sleep(0.5)
    task_step = 0
    while task_step == 0:
        if emulator.find_and_click(f'周常任务'):
            task_step += 1
    if task_step == 1:
        for _ in range(90):
            emulator.click((1122, 140))
            time.sleep(0.5)


@emulator.dir_decorator
def 公开招募():
    abs_tags = ['高级资深干员', '资深干员', '控场', '位移', '特种干员', '快速复活', '支援', '削弱']
    去首页()
    while True:
        if not emulator.find_img('在公招'):
            emulator.find_and_click(['公招', '聘用'])
            emulator.click((1232, 46))
        else:
            if emulator.find_with('聘用', '在公招') == 1:
                break  # 没有可以收取的
    poss = [(400, 375), (600, 375), (750, 375),
            (410, 460), (600, 460)]  # 5个tag的位置

    while True:
        if emulator.find_with([f'招募{i}' for i in range(1, 5)], '在公招') == 1:
            break
        tags = []
        pos = -1
        while True:
            emulator.find_and_click([f'招募{i}' for i in range(1, 5)])
            if emulator.find_img('正在招募'):
                # tags = 识别招募()
                break
        for j in abs_tags:
            if pos != -1:
                break
            for i in range(len(tags)):
                if j == tags[i]:
                    pos = i
                    break
        emulator.click(poss[pos])
        emulator.click((454, 292))
        emulator.click((454, 292))
        step = 0
        while step == 0:
            emulator.find_and_click('蓝底白勾')
            if emulator.find_img('在公招'):
                break  # 没有可以收取的


@emulator.dir_decorator
def 循环招募():
    abs_tags = ['高级资深干员', '资深干员', '控场', '位移', '特种干员', '快速复活', '支援', '削弱']
    xys = [(327, 287), (954, 294), (325, 576), (963, 579)]
    poss = [(400, 375), (600, 375), (750, 375), (410, 460), (600, 460)]
    while True:
        tags = []
        pos = -1
        while True:
            if emulator.find_img('在公招'):
                emulator.click(xys[0])
                time.sleep(1)
            if emulator.find_img('正在招募'):
                # tags = 识别招募()
                break
        for j in abs_tags:
            if pos != -1:
                break
            for i in range(len(tags)):
                if j == tags[i]:
                    pos = i
                    break
        emulator.click(poss[pos])
        emulator.click((454, 292))
        emulator.click((454, 292))

        step = 0
        while step == 0:
            if emulator.find_and_click('蓝底白勾'):
                step += 1
        while step == 1:
            if emulator.find_and_click('立即招募'):
                step += 1
        while step == 2:
            if emulator.find_and_click('红底白勾'):
                step += 1
        while step == 3:
            if emulator.find_and_click('聘用'):
                step += 1
        while step == 4:
            emulator.click((1232, 46))
            if emulator.find_with(['聘用', '立即招募'], '在公招') == 1:
                break  # 没有可以收取的


def 识别招募():
    pass
#     _xys = [(384, 369, 507, 400), (551, 369, 674, 400), (718, 369, 841, 400),
#             (384, 440, 507, 474), (551, 440, 674, 474)]  # 招募tag截图的位置
#     imgs = emulator.take_img(_xys)
#     _res = []
#     for i in range(len(imgs)):
#         imgs[i].save(f'{i}.jpg')
#         f = open(f'{i}.jpg', 'rb')
#         _tmp = f.read()
#         _res.append(emulator.orc.recognize(_tmp))
#         f.close()
#         os.remove(f'{i}.jpg')
#     return _res


@emulator.dir_decorator
def 剿灭():
    if weekly.check('剿灭'):
        return True

    def 检查():
        _res = False
        while True:
            emulator.find_and_click('每周报酬')
            if emulator.find_img('长期剿灭委托'):
                if emulator.find_img('完成剿灭'):
                    weekly.finish('剿灭')
                    _res = True
                else:
                    _res = False
                break
        while not emulator.find_img('剿灭已选择'):
            emulator.find_and_click(['潮没海滨', '长期剿灭委托'], [(0, 0), (-50, 100)])
            time.sleep(1)
        return _res

    去战斗()
    while not emulator.find_img('剿灭已选择'):
        emulator.find_and_click(['剿灭作战', '汐斯塔'])
        time.sleep(1)
    if 检查():
        return True

    _tmp = True
    while _tmp:
        state = 0
        if 检查():
            break
        while state == 0:
            emulator.find_and_click('未代理', (50, 20))
            if emulator.find_img('已代理'):
                state += 1
        while state == 1:
            if emulator.find_img(f'体力刷完了'):
                for _ in range(3):
                    time.sleep(1)
                    emulator.find_and_click(f'体力刷完了')
                    _tmp = False
                    state = 0
                break
            if emulator.find_img(f'战斗中'):
                time.sleep(300)
                state += 1
            emulator.find_and_click(['未代理', '已代理', '开始行动'], [
                                    (50, 20), (50, 70), (0, 0)])
        while state == 2:
            time.sleep(3)
            emulator.find_and_click(['战斗完成1', '战斗完成2', '战斗完成3'], [
                                    (0, -200), (0, -200), (0, -200)])
            if emulator.find_img('已代理'):
                state = 0


def main_script():
    emulator.connect()
    登录方舟()
    基建收菜()
    基建换班()
    使用无人机()
    剿灭()
    刷土()
    # 选择关卡()
    循环挑战()
    信用点()
    # 公开招募()
    收日常任务()
    结束()


def ark_run(tasks):
    emulator.connect()
    for i in tasks:
        exec(f'{i}()')


if __name__ == "__main__":
    a = [

        "循环挑战"

    ]
    ark_run(a)