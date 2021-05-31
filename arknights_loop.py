# !/usr/bin/python
# coding:utf-8

import logging
import time

from orc import *
from config import *
from emulator import Emulator
from arknights_scripts import *

logger = get_logger()
emulator = Emulator(ARKNIGHTS_IMG_PATH)
log_list = ['剿灭', '周任务']
weekly = Periodic(log_list, 'Arknights', 7)


if __name__ == "__main__":
    loop()
