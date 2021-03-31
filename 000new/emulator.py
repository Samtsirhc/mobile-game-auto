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
        try:
            self.emulator = u2.connect()    # python -m uiautomator2 init
            self.window_size = self.emulator.window_size()
            self.img_path = img_path
            self.current_dir = ''
            self.load_imgs()

        except Exception as e:
            logger.error(e)

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
    
    def find_img(self, img, mode = 0):
        '''
        当传入list时，返回bool
        否则mode:0,返回bool;1,返回坐标
        
        '''
        self.screen_shot = self.emulator.screenshot(format="opencv")
        if type(img) == list:
            for i in img:
                _img = self.imgs[self.current_dir][i]
                self.img_coordinate = match_image(_img, self.screen_shot)
                if self.img_coordinate[0] > 0:
                    return True
            return False
        else:
            _img = self.imgs[self.current_dir][img]
            self.img_coordinate = match_image(_img, self.screen_shot)
            logger.debug(f'{img} {self.img_coordinate}')

            if mode == 0:
                if self.img_coordinate[0] > 0:
                    return True
                else:
                    return False
            else:
                return self.img_coordinate
        
    def click(self, coordinate, offset=(0, 0)):
        if coordinate[0] > 0 and coordinate[1] > 0:
            self.emulator.click(
                (coordinate[0] + offset[0]),
                (coordinate[1] + offset[1]))
            return True
        return False
    
    def find_and_click(self, img, offset=(0, 0)):
        tmp = False
        if type(img) == list:
            for i in img:
                if self.click(self.find_img(i, 1)):
                    tmp = True
            return tmp
        else:
            self.img_name = img
            self.click(self.find_img(img, 1), offset)
            if self.img_coordinate[0] > 0:
                return True
            else:
                return False

    def input_text(self, text):
        self.emulator.send_keys(text)

    def swipe(self, xyxy):
        """
        xyxy=(x1,y1,x2,y2),swipe from x1y1 to x2y2
        """
        self.emulator.swipe(xyxy[0], xyxy[1], xyxy[2], xyxy[3])
        
if  __name__ == "__main__":

    pass
