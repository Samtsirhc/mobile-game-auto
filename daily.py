import time

from arknights_scripts import *
from config import *
from pcr_scripts import *
from tools.process_tools import *


def pcr_daily():
    # common_step()
    登录PCR()
    地下城()
    MANA冒险()
    经验值冒险()
    点赞()
    求装备()

def ark_daily():
    # common_step()
    登录方舟()
    基建收菜()
    基建换班()
    使用无人机()
    刷土()
    循环挑战()
    信用点()
    去首页()
    收日常任务()

def common_step():
    close_process("Nox.exe")
    time.sleep(5)  
    run_sth(EMULATOR_PATH)
    time.sleep(30)

if __name__ == '__main__':
    pcr_daily()
    ark_daily()
    time.sleep(7*3600)
    ark_daily()
    time.sleep(7*3600)
    ark_daily()

