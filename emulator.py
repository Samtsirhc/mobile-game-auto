import os
import string
import sys
import time
from threading import Thread
import io
import numpy as np
# import adbutils
# import websocket
import uiautomator2 as u2
from cv2 import cv2
from PIL import Image

from orc import *
from config import *
from tools.image_tools import *
from tools.process_tools import *
from tools.time_tool import *

logger = get_logger()


class Emulator:
    def __init__(self, img_path):
        # self.init_shot()
        self.img_path = img_path
        self.current_dir = ''
        self.load_imgs()


    def connect(self):
        if check_process("Nox.exe"):
            pass
        else:
            logger.info('启动模拟器')
            run_sth(EMULATOR_PATH)
            time.sleep(30)
        self.emulator = u2.connect()    # python -m uiautomator2 init

    def dir_decorator(self, func):
        _no_log = ['进入基建', '去战斗']

        def dec():
            _tmp_dir_name = self.current_dir
            self.current_dir = func.__name__
            func()
            if func.__name__ in _no_log:
                pass
            else:
                logger.info(func.__name__)
            self.current_dir = _tmp_dir_name
        return dec

    def kill_app(self, app_name):
        self.emulator.app_stop(app_name)
        logger.debug(f'{app_name} dead')

    def load_imgs(self):
        self.imgs = {}
        self.img_dirs = get_files(self.img_path, 1)
        for i in self.img_dirs:
            _img_sub_dir = f'{self.img_path}{i}//'
            self.imgs[i] = {}
            for j in get_files(_img_sub_dir, 2):
                _tmp = j.replace('.jpg', '')
                self.imgs[i][_tmp] = {}
                self.imgs[i][_tmp]['img'] = load_img(
                    f'{self.img_path}{i}//{_tmp}')
                self.imgs[i][_tmp]['coordinate'] = (-1, -1)

    def run_app(self, app_name):
        try:
            self.kill_app(app_name)
            self.emulator.app_start(app_name)
            # logger.info("a")
            logger.debug(f'{app_name} start')
        except Exception as e:
            logger.error(e)
        # "com.hypergryph.arknights"

    def check_app(self, app_name):
        _dict = self.emulator.app_current()
        if _dict['package'] == app_name:
            return True
        else:
            return False

    def take_shot(self):
        # try:
        #     _tmp = self.ws.recv()
        #     nparr = np.fromstring(_tmp, np.uint8)
        #     self.screen_shot = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # except:
        #     self.init_shot()
        self.screen_shot = self.emulator.screenshot(format = 'opencv')


    def take_img(self, xys):
        '''
        截图并且返回图片，目前专用于方舟公招
        ''' 
        _img = self.emulator.screenshot()
        _imgs = [_img.crop(i) for i in xys]
        return _imgs


    def find_img(self, img):
        self.take_shot()
        _tmp = False
        if type(img) != list:
            img = [img]
        for i in img:
            _img = self.imgs[self.current_dir][i]['img']
            _xy = match_image(_img, self.screen_shot)
            self.imgs[self.current_dir][i]['coordinate'] = _xy
            logger.debug(f'{i} {_xy}')
            if _xy[0] > 0:
                _tmp = True
        return _tmp
    

    def find_with(self, img, bg):
        '''
        返回值：
        0. 没有bg
        1. 有bg没有img
        2. 有bg有img
        '''
        self.take_shot()
        _tmp = 0
        _img = self.imgs[self.current_dir][bg]['img']
        _xy = match_image(_img, self.screen_shot)
        self.imgs[self.current_dir][bg]['coordinate'] = _xy
        logger.debug(f'{bg} {_xy}')
        if _xy[0] > 0:
            _tmp = 1
            if type(img) != list:
                img = [img]
            for i in img:
                _img = self.imgs[self.current_dir][i]['img']
                _xy = match_image(_img, self.screen_shot)
                self.imgs[self.current_dir][i]['coordinate'] = _xy
                logger.debug(f'{i} {_xy}')
                if _xy[0] > 0:
                    _tmp = 2
        return _tmp


    def click(self, coordinate, offset=(0, 0)):
        if coordinate[0] > 0 and coordinate[1] > 0:
            self.emulator.click(
                (coordinate[0] + offset[0]),
                (coordinate[1] + offset[1]))
            return True
        return False

    def find_and_click(self, img, offset=(0, 0)):
        _tmp = False
        if type(img) == list:
            self.find_img(img)
            if type(offset) == list:
                pass
            else:
                offset = [(0, 0)] * len(img)
            for i in img:
                if self.imgs[self.current_dir][i]['coordinate'][0] > 0:
                    self.click(self.imgs[self.current_dir][i]
                               ['coordinate'], offset[img.index(i)])
                    _tmp = True
        else:
            if self.find_img(img):
                self.click(self.imgs[self.current_dir]
                           [img]['coordinate'], offset)
                _tmp = True
        return _tmp

    def input_text(self, text):
        self.emulator.send_keys(text)

    def swipe(self, xyxy):
        """
        xyxy=(x1,y1,x2,y2),swipe from x1y1 to x2y2
        """
        self.emulator.swipe(xyxy[0], xyxy[1], xyxy[2], xyxy[3])

    # def init_shot(self):
    #     self.d = adbutils.adb.device()
    #     self.lport = self.d.forward_port(7912)
    #     self.ws = websocket.WebSocket()
    #     self.ws.connect("ws://localhost:{}/minicap".format(self.lport))
    #     for _ in range(3):
    #         self.take_shot()
    #     logger.debug('shot manager done')

if __name__ == "__main__":
    e = Emulator(ARKNIGHTS_IMG_PATH)
    e.connect()

    pass
