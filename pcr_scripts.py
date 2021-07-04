import logging
import os
import sys
import time

from cv2 import cv2

from config import get_logger
from emulator import Emulator
from modules.periodic import Periodic
from modules.tools import load_img
from team import TeamManager
from unit import UnitManager

log_list = ["MANA冒险", "经验值冒险", "地下城", "点赞", "JJC", "PJJC"]
daily = Periodic(log_list, 'PCR', 1, 'logs/')
img_path = 'imgs/pcr/'
emulator = Emulator(img_path)
START_APP_NAME = "com.netease.uu"
APP_NAME = "tw.sonet.princessconnect"
logger = get_logger()


class JJCSearcher:
    def __init__(self):
        self.u = UnitManager()
        self.t = TeamManager()
        self._tmp = '_tmp.jpg'

    def search(self, team):
        _team = []
        for i in team:
            i.save(self._tmp)
            _tmp = load_img(self._tmp)
            _team.append(self.u.reg_wife(_tmp))
        return self.t.serch(_team)

    def get_img(self, name, size=100):
        _tmp = self.u.get_img(name, 1)
        _imgs = [cv2.resize(i, (115, 115)) for i in _tmp]
        return _imgs


searcher = JJCSearcher()


@emulator.dir_decorator
def 登录PCR():
    emulator.run_app(START_APP_NAME)
    while not emulator.check_app(APP_NAME):
        emulator.find_and_click(['我的', '加速'], [(-230, 10), (578, 37)])
    while not emulator.find_img('商店'):
        time.sleep(1)
        emulator.find_and_click(['下载', '关闭', '生日快乐'])
        emulator.click((650, 620))
        if emulator.find_img('请选择角色'):
            兰德索尔杯()
        if emulator.find_img('签筒'):
            emulator.swipe((540, 500, 540, 250))
    while True:
        time.sleep(1)
        emulator.click((650, 620))
        if emulator.find_img('商店'):
            # 登录成功
            break


def 找解法():
    _xys = [(783, 114, 854, 156),
            (873, 114, 944, 156),
            (963, 114, 1034, 156),
            (1053, 114, 1124, 156),
            (1143, 114, 1214, 156)]
    _team = emulator.take_img(_xys)
    return searcher.search(_team)


def 选择进攻队伍(used=None):
    _my_team = ["優花梨", "咲戀", "初音", "似似花", "露娜"]
    _teams = 找解法()
    _team = []
    if len(_teams) < 1:
        _team = _my_team
    for i in _teams:
        if searcher.t.check_unget(i, used=used):
            _team = i
            break
    选择角色(_team)
    return _team


def 结束():
    emulator.kill_app(APP_NAME)
    emulator.kill_app(START_APP_NAME)


@emulator.dir_decorator
def 兰德索尔杯():
    for _ in range(3):
        time.sleep(1)
        emulator.click((266, 400))
    while True:
        if emulator.find_and_click('比赛开始'):
            return


@ emulator.dir_decorator
def 去冒险():
    while True:
        emulator.find_and_click('冒险未激活')
        emulator.click((644, 655))
        time.sleep(0.5)
        if emulator.find_img('冒险已激活'):
            # 处于冒险页面
            break


@ emulator.dir_decorator
def 去主页():
    while True:
        emulator.click((121, 655))
        time.sleep(0.5)
        if emulator.find_img('主页已激活'):
            # 处于主页
            break


@ emulator.dir_decorator
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


@ emulator.dir_decorator
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


@ emulator.dir_decorator
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


@ emulator.dir_decorator
def 进入商店():
    去主页()
    while True:
        emulator.find_and_click('商店')
        if emulator.find_img('在商店'):
            break


@ emulator.dir_decorator
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


@ emulator.dir_decorator
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


@ emulator.dir_decorator
def 持续战斗():
    while True:
        time.sleep(3)
        emulator.find_and_click(['妈2', '妈', '进行挑战', '战斗开始', '下一步', '关闭', '取消'])


@ emulator.dir_decorator
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


@ emulator.dir_decorator
def 求装备():
    去主页()
    while True:
        emulator.find_and_click(['请求结果', 'OK', '战队', '白底OK', '装备请求', '请求'])
        if emulator.find_img(['请求状况', '无战队']):
            break


@ emulator.dir_decorator
def JJC():  # 未完成
    if daily.check('JJC'):
        return None
    去冒险()
    for _ in range(5):
        state = 0
        while state == 0:
            if emulator.find_img('在竞技场'):
                state += 1
                break
            emulator.find_and_click(['战斗竞技场', '防御结果'], [(0, 0), (-209, 22)])
        while state == 1:
            if not emulator.find_img('冷却完成'):
                time.sleep(15)
            else:
                emulator.find_and_click('更新清单')
                state += 1
                time.sleep(5)
        while state == 2:
            if not emulator.find_img('在竞技场'):
                state += 1
                time.sleep(3)
            else:
                emulator.click((1188, 186))
        while state == 3:
            emulator.find_and_click(['战斗开始', '下一步'])
            if emulator.find_img('在竞技场'):
                state += 1
    daily.finish('JJC')


@ emulator.dir_decorator
def PJJC():
    if daily.check('PJJC'):
        return None
    去冒险()
    for _ in range(5):
        state = 0
        while state == 0:
            if emulator.find_img('在竞技场'):
                state += 1
            emulator.find_and_click(['公主竞技场', '防御结果'], [(0, 0), (-209, 22)])
        while state == 1:
            if not emulator.find_img('冷却完成'):
                time.sleep(15)
            else:
                emulator.find_and_click('更新清单')
                state += 1
                time.sleep(5)
        while state == 2:
            if not emulator.find_img('在竞技场'):
                state += 1
                time.sleep(3)
            else:
                emulator.click((1188, 186))
        while state == 3:
            emulator.find_and_click(['队伍2', '队伍3', '战斗开始', '下一步'])
            if emulator.find_img('在竞技场'):
                state += 1
    daily.finish('PJJC')


@ emulator.dir_decorator
def 选择角色(names):
    '''
    五个！
    '''
    def choose_wife(name):
        _tmp = 0
        while _tmp == 0:
            emulator.find_and_click('以角色名搜寻')
            if emulator.find_img('确定'):
                _tmp += 1
        while _tmp == 1:
            emulator.input_text(name)
            time.sleep(0.5)
            emulator.click((153, 355))
            time.sleep(1)
            _tmp += 1
        while _tmp == 2:
            _xys = [(92, 351, 202, 418), (232, 351, 342, 418),
                    (372, 351, 482, 418), (512, 351, 622, 418),
                    (652, 351, 762, 418), (792, 351, 902, 418)]
            _ponits = [(151, 389), (291, 389), (433, 389),
                       (574, 389), (751, 389), (856, 389)]
            _imgs = emulator.take_img(_xys)
            _p = 0
            for i in range(len(_imgs)):
                _img = _imgs[i]
                _img.save("_tmp.jpg")
                _img = load_img("_tmp.jpg")
                os.remove("_tmp.jpg")
                _res = searcher.u.reg_wife(_img, 125)
                if _res == name:
                    _p = i
                    break
            else:
                print(f'没找到 {name}')
            emulator.click(_ponits[_p])
            time.sleep(0.5)
            if emulator.find_img('以角色名搜寻'):
                _tmp += 1
            else:
                emulator.click(_ponits[_p])
                time.sleep(0.5)

    while not emulator.find_img('我的队伍'):
        time.sleep(0.5)
    if emulator.find_img('重置'):
        pass
    else:
        emulator.swipe((634, 250, 634, 450))
        time.sleep(1)
    for i in names:
        choose_wife(i)
    pass


@ emulator.dir_decorator
def 打双场():
    if daily.check('JJC') and daily.check('PJJC'):
        return None

    def 打JJC():
        if daily.check('JJC'):
            return
        去冒险()
        _step = 0
        while _step == 0:
            emulator.find_and_click(['战斗竞技场'])
            if emulator.find_img('更新清单'):
                _step += 1
        while _step == 1:
            if emulator.find_img(['冷却完成', '冷却完成2']):
                _step += 1
            else:
                time.sleep(1)
        while _step == 2:
            emulator.find_and_click('更新清单', (16, 93))
            if emulator.find_img('次数上限'):
                daily.finish('JJC')
                return
            if emulator.find_img('我的队伍'):
                # 清空角色栏
                for _ in range(10):
                    emulator.click((715, 600))
                    time.sleep(0.1)
                _step += 1
        选择进攻队伍()
        while _step == 3:
            emulator.find_and_click(['战斗开始', '下一步'])
            if emulator.find_img('更新清单'):
                _step += 1
            time.sleep(3)

    def 打PJJC():
        if daily.check('PJJC'):
            return
        去冒险()
        _step = 0
        while _step == 0:
            emulator.find_and_click(['公主竞技场'])
            if emulator.find_img('更新清单'):
                _step += 1
        while _step == 1:
            if emulator.find_img(['冷却完成', '冷却完成2']):
                _step += 1
            else:
                time.sleep(1)
        while _step == 2:
            emulator.find_and_click('更新清单', (-16, 93))
            if emulator.find_img('次数上限'):
                daily.finish('PJJC')
                return
            if emulator.find_img('我的队伍'):
                _step += 1
        _used = searcher.t.unget_roles.copy()
        _teams = []
        if _step == 3:
            # 清空队伍
            for _ in range(3):
                for _ in range(10):
                    emulator.click((715, 600))
                    time.sleep(0.1)
                emulator.click((1121, 600))
            while not emulator.find_and_click('队伍1激活'):
                emulator.click((128, 115))
                time.sleep(0.5)
                pass
            if emulator.find_with('问号', '我的队伍') == 2:
                # 第一队不可见
                _teams, _rate = searcher.t.get_best_teams(_used, 3)
            else:
                # 第一队可见
                _teams = 找解法()
                if _teams == []:
                    _teams, _rate = searcher.t.get_best_teams(_used, 3)
                else:
                    _teams_list = []
                    for i in range(len(_teams)):
                        _team1 = [_teams[i]]
                        _used_ = _used.copy() + _team1[0]
                        _team23, _rate_ = searcher.t.get_best_teams(_used_, 2)
                        _teams_list.append({'teams':_team1 + _team23, 'rate':_rate_})
                        if _rate_ > 1.99:
                            break
                    _teams_list = sorted(_teams_list, key=lambda i: i['rate'], reverse=True)
                    _teams = _teams_list[0]['teams']
                    _rate = _teams_list[0]['rate'] + 1.0
            logger.info(f'胜率{_rate}，队伍{_teams}')
            选择角色(_teams[0])
            while True:
                emulator.find_and_click('队伍2')
                time.sleep(1)
                if emulator.find_img('队伍3'):
                    break
            选择角色(_teams[1])
            while True:
                emulator.find_and_click('队伍3')
                time.sleep(1)
                if emulator.find_img('战斗开始'):
                    break
            选择角色(_teams[2])
            _step += 1
        while _step == 4:
            emulator.find_and_click('战斗开始')
            if emulator.find_img('下一步'):
                _step += 1
            else:
                time.sleep(3)
        if _step == 5:
            _fight_res = []

            _oxy = (316, 225, 394, 281)
            _dx = 116
            _dy = 142
            _xy11 = [(_oxy[0] + i*_dx, _oxy[1], _oxy[2] + i*_dx, _oxy[3])
                     for i in range(5)]
            _xy22 = [(_oxy[0] + i*_dx, _oxy[1]+_dy, _oxy[2] +
                      i*_dx, _oxy[3]+_dy) for i in range(5)]
            _xy33 = [(_oxy[0] + i*_dx, _oxy[1]+_dy*2, _oxy[2] +
                      i*_dx, _oxy[3]+_dy*2) for i in range(5)]
            _xy1 = [(68, 202, 291, 312)] + _xy11
            _xy2 = [(68, 342, 291, 452)] + _xy22
            _xy3 = [(68, 482, 291, 592)] + _xy33

            _res1 = emulator.take_img(_xy1)
            _res2 = emulator.take_img(_xy2)
            _res3 = emulator.take_img(_xy3)
            _res = [_res1, _res2, _res3]

            _count_game = [0,0,0]
            for i in _res:
                _count_game[0] += 1
                i[0].save('_tmpp.jpg')
                _tmpp = load_img('_tmpp.jpg')
                if emulator.find_img(img='lose', bg=_tmpp):
                    _result = False
                    _count_game[1] += 1
                else:
                    _result = True
                    _count_game[2] += 1
                _team = []
                for j in range(1, len(i)):
                    i[j].save('_tmpp.jpg')
                    _tmpp = load_img('_tmpp.jpg')
                    _team.append(searcher.u.reg_wife(_tmpp, 96))
                searcher.t.report_pjjc_result(_team, _result)
                if _count_game[0] == 2 and (_count_game[1] == 2 or _count_game[2] == 2):
                    break
            os.remove('_tmpp.jpg')
            _step += 1
        while _step == 6:
            emulator.find_and_click('下一步')
            if emulator.find_img('更新清单'):
                _step += 1

    打PJJC()


def pcr_run(tasks):
    emulator.connect()
    for i in tasks:
        exec(f'{i}()')


if __name__ == "__main__":
    # logger.setLevel(logging.DEBUG)
    emulator.connect()
    for _ in range(99):
        打双场()
