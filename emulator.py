import os
import string
import time
import io
import adbutils
import numpy as np
import uiautomator2 as u2
import websocket
from cv2 import cv2
from PIL import Image

from config import get_logger
from modules.image_tool import load_img, match_image
from modules.orc import Orc
from modules.path_tool import get_files
from modules.process_tool import check_process, run

logger = get_logger()


class Emulator:
    def __init__(self, img_path=''):
        # self.init_shot()
        if img_path == '':
            return
        self.img_path = img_path
        self.current_dir = ''
        self.load_imgs()
        # self.orc = Orc()
        self.no_log = ['进入基建', '去战斗', '去冒险', '去首页', '选择角色']

    def connect(self):
        em_name =  'Nox' # 'Nox' 'dnplayer'
        if check_process(f"{em_name}.exe"):
            pass
        else:
            run(f'%USERPROFILE%/Desktop/{em_name}.lnk')
            logger.info('启动模拟器')
            time.sleep(30)
        self.emulator = u2.connect()  # python -m uiautomator2 init

    def dir_decorator(self, func):
        def dec(*args, **kwargs):
            _tmp_dir_name = self.current_dir
            self.current_dir = func.__name__
            func(*args, **kwargs)
            if func.__name__ in self.no_log:
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

    def init_shot(self):
        d = adbutils.adb.device()
        lport = d.forward_port(7912)
        self.ws = websocket.WebSocket()
        self.ws.connect("ws://localhost:{}/minicap".format(lport))

    def take_shot(self):
        # try:
        #     _tmp = self.ws.recv()
        #     while not isinstance(_tmp, (bytes, bytearray)):
        #         _tmp = self.ws.recv()
        # except:
        #     self.init_shot()
        #     _tmp = self.ws.recv()
        #     while not isinstance(_tmp, (bytes, bytearray)):
        #         _tmp = self.ws.recv()

        # for _ in range(100):
        #     with open('_tmp.jpg', 'wb') as f:     # 百次 3.2s
        #         f.write(_tmp)
        #     self.screen_shot = load_img('_tmp.jpg')

        # with open('_tmp.jpg', 'wb') as f:     # 百次 25.5s
        #     f.write(_tmp)
        # self.screen_shot = load_img('_tmp.jpg')
        # os.remove('_tmp.jpg')

        _tmp = self.emulator.screenshot(format='raw')  # 百次 232.9s
        _tmp = np.fromstring(_tmp, np.uint8)
        self.screen_shot = cv2.imdecode(_tmp, cv2.IMREAD_COLOR)
        return self.screen_shot

    def take_img(self, xys):
        """
        截图并且返回图片，目前专用于方舟公招
        例如xys = [(384, 369, 507, 400), (551, 369, 674, 400)]
        """
        _img = self.emulator.screenshot()
        _imgs = [_img.crop(i) for i in xys]
        return _imgs

    def find_imgs(self, img):
        """
        找一张图有多少个
        """
        self.take_shot()
        _img = self.imgs[self.current_dir][img]['img']
        _xy = match_image(_img, self.screen_shot, 0.95, True)
        logger.debug(f'{img} {_xy}')
        return _xy

    def find_img(self, img, return_type = 0, bg = 0):
        self.take_shot()
        _tmp = False
        if type(img) != list:
            img = [img]
        if type(bg) == int:
            bg = self.screen_shot
        for i in img:
            if type(i) == str:
                _img = self.imgs[self.current_dir][i]['img']
                _xy = match_image(_img, bg)
                self.imgs[self.current_dir][i]['coordinate'] = _xy
                logger.debug(f'{i} {_xy}')
                if self.check_img_xy(i):
                    _tmp = True
            else:
                _xy = match_image(i, bg)
                logger.debug(f'{_xy}')
                if _xy[0] > 0:
                    _tmp = True
                    if return_type == 1 :
                        _tmp = _xy
        return _tmp

    def check_img_xy(self, img):
        try:
            if self.imgs[self.current_dir][img]['coordinate'][0] > 0:
                return True
            else:
                return False
        except KeyError:
            if self.imgs['common'][img]['coordinate'][0] > 0:
                return True
            else:
                return False

    def find_with(self, img, bg):
        """
        返回值：
        0. 没有bg
        1. 有bg没有img
        2. 有bg有img
        """
        _tmp = 0
        if type(img) != list:
            img = [img]
        img.append(bg)
        self.find_img(img)
        if self.check_img_xy(img[-1]):
            _tmp = 1
            for i in range(len(img) - 1):
                if self.check_img_xy(img[i]):
                    _tmp = 2
        else:
            pass
        return _tmp

    def clicks(self, coordinate, offset=(0, 0)):
        for _xy in range(len(coordinate)):
            time.sleep(0.5)
            a = int(coordinate[-_xy][0])
            b = int(coordinate[-_xy][1])
            self.click((a, b), offset)

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


if __name__ == "__main__":
    run('%USERPROFILE%/Desktop/1.txt')
    pass
