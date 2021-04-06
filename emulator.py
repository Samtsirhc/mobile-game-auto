import os
import string
import sys
import time
from threading import Thread

import uiautomator2 as u2

from config import *
from tools.image_tools import *
from tools.time_tool import *

logger = get_logger()
class Emulator:
    def __init__(self, img_path):
        self.emulator = u2.connect()    # python -m uiautomator2 init
        self.window_size = self.emulator.window_size()
        self.img_path = img_path
        self.current_dir = ''
        self.load_imgs()

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
                self.imgs[i][_tmp] = load_img(f'{self.img_path}{i}//{_tmp}')


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

    def find_img(self, img):
        self.screen_shot = self.emulator.screenshot(format="opencv")
        time.sleep(0.5)
        if type(img) == list:
            for i in img:
                _img = self.imgs[self.current_dir][i]
                self.img_name = i
                self.img_coordinate = match_image(_img, self.screen_shot)
                logger.debug(f'{i} {self.img_coordinate}')
                if self.img_coordinate[0] > 0:
                    return True
            return False
        else:
            # print(self.current_dir);print(img)
            _img = self.imgs[self.current_dir][img]
            self.img_coordinate = match_image(_img, self.screen_shot)
            logger.debug(f'{img} {self.img_coordinate}')
            if self.img_coordinate[0] > 0:
                return True
            else:
                return False
        
    def click(self, coordinate, offset=(0, 0)):
        if coordinate[0] > 0 and coordinate[1] > 0:
            self.emulator.click(
                (coordinate[0] + offset[0]),
                (coordinate[1] + offset[1]))
            return True
        return False
    
    def find_and_click(self, img, offset=(0,0)):
        if type(img) == list:
            if self.find_img(img):
                if type(offset) == tuple:
                    self.click(self.img_coordinate)
                else:
                    self.click(self.img_coordinate, offset[img.index(self.img_name)])
                return True
        else:
            if self.find_img(img):
                self.click(self.img_coordinate, offset)
                return True
        return False

    def input_text(self, text):
        self.emulator.send_keys(text)

    def swipe(self, xyxy):
        """
        xyxy=(x1,y1,x2,y2),swipe from x1y1 to x2y2
        """
        self.emulator.swipe(xyxy[0], xyxy[1], xyxy[2], xyxy[3])
        
if  __name__ == "__main__":
    e = Emulator(ARKNIGHTS_IMG_PATH)
    print(e.check_app(ARKNIGHTS_APP_NAME))
    pass
