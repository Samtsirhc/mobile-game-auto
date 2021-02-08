import time
import logging
from emulator import Emulator
from pcr_scripts import *
from tools.process_tools import *

def 完整日常流程():
    if check_process('Nox.exe'):
        pass
    else:
        run_sth('PCR.lnk')
        time.sleep(60)
    emulator = Emulator()
    登录PCR(emulator)
    地下城(emulator)
    MANA冒险(emulator)
    经验值冒险(emulator)
    close_process("Nox.exe")

if __name__ == "__main__":
    完整日常流程()
    pass
