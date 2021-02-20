from config import *
from emulator import Emulator
from pcr_scripts import *
from arknights_scripts import *
from tools.process_tools import *

def common_step():
    close_process("Nox.exe")
    time.sleep(5)  
    run_sth(EMULATOR_PATH)
    time.sleep(60)

def PCR日常():
    common_step()
    emulator = Emulator()
    登录PCR(emulator)
    地下城(emulator)
    MANA冒险(emulator)
    经验值冒险(emulator)
    close_process("Nox.exe")

def 方舟日常():
    common_step()
    emulator = Emulator()
    登录方舟(emulator)
    进入基建(emulator)
    基建换班(emulator)
    进入基建(emulator)  # 换班完了回到基建大厅 
    基建收菜(emulator)
    使用无人机(emulator)
    去战斗(emulator)
    # 刷经验(emulator)
    画中人(emulator)
    循环挑战(emulator)
    去首页(emulator)
    信用点(emulator)
    去首页(emulator)    # 信用搞完了回首页
    收日常任务(emulator)
    close_process("Nox.exe")
    
if __name__ == "__main__":
    # PCR日常()
    logger = get_logger()
    logger.setLevel(logging.DEBUG)
    方舟日常()
    pass
