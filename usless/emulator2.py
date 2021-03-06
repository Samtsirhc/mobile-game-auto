import uiautomator2 as u2
import time

from modules.orc import Orc
from modules.process_tool import check_process, close_process, run, run_sth
from modules.logger import Logger


class Emulator:
    def __init__(self, img_path, logger:Logger):
        self.orc = Orc()
        self.logger = logger
        self.no_log = ['进入基建', '去战斗', '去冒险', '去首页', '选择角色']


    def connect(self, emulator_path):
        if check_process("Nox.exe"):
            pass
        else:
            self.logger.info('启动模拟器')
            run_sth(emulator_path)
            time.sleep(30)
        self.emulator = u2.connect()  # python -m uiautomator2 init

    def dir_decorator(self, func):
        def dec(*args,**kwargs):
            _tmp_dir_name = self.current_dir
            self.current_dir = func.__name__
            func(*args,**kwargs)
            if func.__name__ in self.no_log:
                pass
            else:
                self.logger.info(func.__name__)
            self.current_dir = _tmp_dir_name

        return dec

    def kill_app(self, app_name):
        self.emulator.app_stop(app_name)
        self.logger.debug(f'{app_name} dead')

    # def load_imgs(self):
    #     self.imgs = {}
    #     self.img_dirs = get_files(self.img_path, 1)
    #     for i in self.img_dirs:
    #         _img_sub_dir = f'{self.img_path}{i}//'
    #         self.imgs[i] = {}
    #         for j in get_files(_img_sub_dir, 2):
    #             _tmp = j.replace('.jpg', '')
    #             self.imgs[i][_tmp] = {}
    #             self.imgs[i][_tmp]['img'] = load_img(
    #                 f'{self.img_path}{i}//{_tmp}')
    #             self.imgs[i][_tmp]['coordinate'] = (-1, -1)

    def run_app(self, app_name):
        try:
            self.kill_app(app_name)
            self.emulator.app_start(app_name)
            # logger.info("a")
            self.logger.debug(f'{app_name} start')
        except Exception as e:
            self.logger.error(e)
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
        self.screen_shot = self.emulator.screenshot(format='opencv')

    def take_img(self, xys):
        """
        截图并且返回图片，目前专用于方舟公招
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
            if self.check_img_xy(i):
                _tmp = True
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
    e = Emulator(ARKNIGHTS_IMG_PATH)
    e.connect()

    pass
