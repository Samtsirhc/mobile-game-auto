import os
import sys
import time
import string
import uiautomator2 as u2

from tools.image_tools import match_image
from config import get_logger

logger = get_logger()

class Emulator:
    def __init__(self, auto_task=False, auto_policy=True,
                 auto_goods=False, speedup=True):
        try:
            self.emulator = u2.connect()    # python -m uiautomator2 init
            self.window_size = self.emulator.window_size()
            self.screen_shot = self.emulator.screenshot(format="opencv")
        except Exception as e:
            logger.error(e)

    def kill_app(self, app_name):
        self.emulator.app_stop(app_name)

    def run_app(self, app_name):
        try:
            self.emulator.app_start(app_name)
            # logger.info("a")
            logger.debug(f'{app_name} start')
        except Exception as e:
            logger.error(e)
        # "com.hypergryph.arknights"

    def find_img(self, img,path: str, return_type=0,screen_shot = ''):
        if type(screen_shot) == str:
            self.screen_shot = self.emulator.screenshot(format="opencv")

        else:
            self.screen_shot = screen_shot
        if type(img) == list:
            for i in img:
                self.img_coordinate = match_image(path + i, self.screen_shot)
                if self.img_coordinate[0] > 0:
                    return True
            return False
        else:
            self.img_coordinate = match_image(path + img, self.screen_shot)
            logger.debug(f'{img} {self.img_coordinate}')
            if self.img_coordinate[0] > 0:
                self.find_result = True
            else:
                self.find_result = False
            if return_type == 0:
                return self.find_result
            else:
                return self.img_coordinate

    def click(self, coordinate, offset=(0, 0)):
        if coordinate[0] > 0 and coordinate[1] > 0:
            self.emulator.click(
                (coordinate[0] + offset[0]),
                (coordinate[1] + offset[1]))

    def find_and_click(self, img, path, offset=(0, 0)):
        if type(img) == list:
            screen_shot = self.emulator.screenshot(format="opencv")
            for i in img:
                self.click(self.find_img(i,path,1,screen_shot))
        else:
            time.sleep(0.3)
            self.img_name = img
            self.click(self.find_img(img, path,1), offset)
            if self.img_coordinate[0] > 0:
                return True
            else:
                return False
        # return self.img_coordinate

    # click image when the mark is exist
    # def click_with_img(self, img, mark, offset=(0, 0)):
    #     if self.find_img(mark):
    #         self.find_and_click(img, offset)

    # def find_with_mark(self, img, mark):
    #     if self.find_img(mark) and self.find_img(img):
    #         return True
    #     else:
    #         return False

    def input_text(self, text):
        self.emulator.send_keys(text)

    def swipe(self, xyxy):
        """
        xyxy=(x1,y1,x2,y2),swipe from x1y1 to x2y2
        """
        self.emulator.swipe(xyxy[0], xyxy[1], xyxy[2], xyxy[3])

if __name__ == "__main__":
    if type(['a','b']) == list:
        print(1)