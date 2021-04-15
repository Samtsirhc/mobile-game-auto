import logging
import os
import sys
import time

import psutil
from orc import *
from config import *
from emulator import Emulator

logger = get_logger()
emulator = Emulator(ARKNIGHTS_IMG_PATH)
log_list = ['剿灭', '周任务']
weekly = Periodic(log_list, 'Arknights', 7)

@emulator.dir_decorator
def 登录方舟():
    emulator.run_app(ARKNIGHTS_APP_NAME)
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


@emulator.dir_decorator
def 进入基建():
    while not emulator.find_img('在基建'):
        if not emulator.find_img('在导航'):
            emulator.find_and_click(['导航基建', '基建'])
        else:
            emulator.find_and_click('导航小房子')
    pass


@emulator.dir_decorator
def 基建换班():
    进入基建()

    # 安排休息
    dorm_order = 1
    state = 0
    while dorm_order < 5:
        if emulator.find_img('进驻总览'):
            emulator.click((830, 200 + 100 * dorm_order))
            time.sleep(1)
        if emulator.find_img('在宿舍'):
            state = 1

        clear_count = 0
        while state == 1:
            emulator.find_and_click('进驻信息')
            if emulator.find_img('在进驻信息'):
                state += 1
        while state == 2:
            if clear_count > 2:
                emulator.find_and_click('进驻')
                if emulator.find_img('在换班'):
                    state += 1
            else:
                if emulator.find_and_click('清空'):
                    clear_count += 1
                    time.sleep(1)
        while state == 3:
            for wife_x in range(5):
                for wife_y in range(2):
                    emulator.click((487 + wife_x * 145, 226 + wife_y * 250))
                    time.sleep(0.1)
            state += 1
        while state == 4:
            emulator.find_and_click(['确认', '红底白勾'])
            if emulator.find_img(f'在进驻信息'):
                emulator.find_and_click('后退')
            if emulator.find_img(f'进驻总览'):
                dorm_order += 1
                state = 0

    # 制造站
    factory_order = 1
    stone = 0
    while factory_order < 4:
        if emulator.find_img('进驻总览'):
            emulator.click((70 + 200 * (factory_order - 1), 310))
            time.sleep(1)
        if emulator.find_img('制造站'):
            state = 1

        clear_count = 0
        while state == 1:
            emulator.find_and_click('进驻信息')
            if emulator.find_img('在进驻信息'):
                state += 1
        while state == 2:
            if clear_count > 2:
                emulator.find_and_click('进驻')
                if emulator.find_img('在换班'):
                    state += 1
            else:
                emulator.find_and_click('红底白勾')
                if emulator.find_and_click('清空'):
                    clear_count += 1
                    time.sleep(1)
        while state == 3:
            for wife_x in range(2):
                for wife_y in range(2):
                    emulator.click((487 + wife_x * 145, 226 + wife_y * 250))
                    time.sleep(0.1)
            state += 1
        while state == 4:
            emulator.find_and_click(['确认', '红底白勾'])
            if emulator.find_img(f'在进驻信息'):
                emulator.find_and_click('后退')
            if emulator.find_img(f'进驻总览'):
                factory_order += 1
                state = 0

    while factory_order == 4 and MINING:
        if emulator.find_img('进驻总览'):
            emulator.click((70, 310))
            time.sleep(1)
        if stone == 0:
            if emulator.find_img('源石'):
                stone = 1
        while stone < 10 and stone > 0:
            if stone == 1:
                emulator.find_and_click('源石')
                if emulator.find_img('固源岩'):
                    stone += 1
            if stone == 2:
                for _ in range(5):
                    emulator.click((962, 206))
                    time.sleep(0.1)
                for _ in range(5):
                    emulator.click((950, 579))
                    time.sleep(0.1)
                stone += 1
            if stone == 3:
                if emulator.find_img(f'进驻总览'):
                    stone += 10
                    factory_order += 1
                else:
                    emulator.click((44, 44))
                    time.sleep(3)

    # 贸易站
    trade_order = 1
    while trade_order < 4:
        if emulator.find_img('进驻总览'):
            emulator.click((10 + 200 * (trade_order - 1), 410))
            time.sleep(1)
        if emulator.find_img('贸易站'):
            state = 1

        clear_count = 0
        while state == 1:
            emulator.find_and_click('进驻信息')
            if emulator.find_img('在进驻信息'):
                state += 1
        while state == 2:
            if clear_count > 2:
                emulator.find_and_click('进驻')
                if emulator.find_img('在换班'):
                    state += 1
            else:
                emulator.find_and_click('红底白勾')
                if emulator.find_and_click('清空'):
                    clear_count += 1
                    time.sleep(1)
        while state == 3:
            for wife_x in range(2):
                for wife_y in range(2):
                    emulator.click((487 + wife_x * 145, 226 + wife_y * 250))
                    time.sleep(0.1)
            state += 1
        while state == 4:
            emulator.find_and_click(['确认', '红底白勾'])
            if emulator.find_img(f'在进驻信息'):
                emulator.find_and_click('后退')
            if emulator.find_img(f'进驻总览'):
                trade_order += 1
                state = 0

    # 发电站
    elect_order = 1
    while elect_order < 4:
        if emulator.find_img('进驻总览'):
            emulator.click((70 + 200 * (elect_order - 1), 510))
            time.sleep(1)
        if emulator.find_img('发电站'):
            state = 1

        clear_count = 0
        while state == 1:
            emulator.find_and_click('进驻信息')
            if emulator.find_img('在进驻信息'):
                state += 1
        while state == 2:
            if clear_count > 2:
                emulator.find_and_click('进驻')
                if emulator.find_img('在换班'):
                    state += 1
            else:
                emulator.find_and_click('红底白勾')
                if emulator.find_and_click('清空'):
                    clear_count += 1
                    time.sleep(1)
        while state == 3:
            for wife_x in range(1):
                for wife_y in range(2):
                    emulator.click((487 + wife_x * 145, 226 + wife_y * 250))
                    time.sleep(0.1)
            state += 1
        while state == 4:
            emulator.find_and_click(['确认', '红底白勾'])
            if emulator.find_img(f'在进驻信息'):
                emulator.find_and_click('后退')
            if emulator.find_img(f'进驻总览'):
                elect_order += 1
                state = 0


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
    while not emulator.find_img('在战斗页面'):
        if emulator.find_img('在导航'):
            emulator.find_and_click('作战')
        else:
            emulator.find_and_click(['导航小房子', '首页作战'])
    pass


@emulator.dir_decorator
def 选择关卡():
    while True:
        if emulator.find_img(f'关卡已选择'):
            break
        emulator.find_and_click(['物资筹备', '战术演习', 'LS-5'])
        # emulator.find_and_click(["源石尘行动","行动记录","OD-6"])
        # emulator.find_and_click(['画中人','入画','WR-3'])
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
    state = 0
    while state == 0:
        if emulator.find_img('左箭头'):
            state += 1
        emulator.find_and_click(['主线','苦难摇篮','怒号光明'])

    while state == 1:
        if not emulator.find_and_click('左箭头'):
            state += 1
    
    while state == 2:
        if not emulator.find_img('在第一章'):
            emulator.find_and_click('右箭头01')
            time.sleep(1.5)
        else:
            state += 1
    
    while state == 3:
        if not emulator.find_and_click('1-7'):
            emulator.swipe((800,360,400,360))
            time.sleep(1.5)
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
    abs_tags = ['高级资深干员','资深干员', '控场','位移', '特种', '快速复活', '支援', '削弱']
    去首页()
    while True:
        if not emulator.find_img('在公招'):
            emulator.find_and_click(['公招', '聘用'])
            emulator.click((1232,46))
        else:
            if emulator.find_with('聘用', '在公招') == 1:
                break   # 没有可以收取的
    count = 1
    xys = [(327,287),(954,294),(325,576),(963,579)]
    poss = [(400,375),(600,375),(750,375),(410,460),(600,460)]
    for i in range(count):
        tags = []
        pos = -1
        while True:
            if emulator.find_img('在公招'):
                emulator.click(xys[i])
                time.sleep(1)
            if emulator.find_img('正在招募'):
                tags = 识别招募()
                break
        for j in abs_tags:
            if pos != -1:
                break
            for i in range(len(tags)):
                if j == tags[i]:
                    pos = i
                    break
        emulator.click(poss[pos])
        for _ in range(11):
            time.sleep(0.1)
            emulator.click((454,152))
        emulator.find_and_click('蓝底白勾')

@emulator.dir_decorator
def 循环招募():
    abs_tags = ['高级资深干员','资深干员', '控场','位移', '特种干员', '快速复活', '支援', '削弱']
    xys = [(327,287),(954,294),(325,576),(963,579)]
    poss = [(400,375),(600,375),(750,375),(410,460),(600,460)]
    while True:
        tags = []
        pos = -1
        while True:
            if emulator.find_img('在公招'):
                emulator.click(xys[0])
                time.sleep(1)
            if emulator.find_img('正在招募'):
                tags = 识别招募()
                break
        for j in abs_tags:
            if pos != -1:
                break
            for i in range(len(tags)):
                if j == tags[i]:
                    pos = i
                    logger.info(tags[i])
                    break
        emulator.click(poss[pos])
        for _ in range(9):
            time.sleep(0.1)
            emulator.click((454,152))
        
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
            emulator.click((1232,46))
            if emulator.find_with(['聘用','立即招募'], '在公招') == 1:
                break   # 没有可以收取的
        

def 识别招募():
    _xys = [(384,369,507,400),(551,369,674,400),(718,369,841,400),(384,440,507,474),(551,440,674,474)]
    imgs = emulator.take_img(_xys)
    _res = []
    for i in range(len(imgs)):
        imgs[i].save(f'{i}.jpg')
        f = open(f'{i}.jpg', 'rb')
        _tmp = f.read()
        _res.append(my_orc(_tmp))
        f.close()
        os.remove(f'{i}.jpg')
    logger.info(_res)
    return _res

@emulator.dir_decorator
@weekly.periodic_manager
def 剿灭():
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
            emulator.find_and_click(['废弃矿区','长期剿灭委托'], [(0,0),(-50, 100)])
            time.sleep(1)
        return _res
    if weekly.check('剿灭'):
        return True


    去战斗()
    while not emulator.find_img('剿灭已选择'):
        emulator.find_and_click(['剿灭作战', '乌萨斯', '废弃矿区'])
        time.sleep(1)
    if 检查():
        return True
    while not emulator.find_img(f'体力刷完了'):
        if emulator.find_img(f'战斗中'):
            time.sleep(60)
        emulator.find_and_click(['未代理', '已代理','开始行动','战斗完成1','废弃矿区'], [(50, 20), (50, 70), (0, 0),(0, -200),(0,0)])
        if emulator.find_and_click('战斗完成2', (0, -200)):
            if 检查():
                break
    for _ in range(3):
        time.sleep(1)
        emulator.find_and_click(f'体力刷完了')



if __name__ == "__main__":
    # logger.setLevel(logging.DEBUG)
    emulator.connect()
    # 循环招募()
    登录方舟()
    基建收菜()
    基建换班()
    使用无人机()
    剿灭()
    刷土()
    循环挑战()
    信用点()
    # 公开招募()
    收日常任务()
