from cv2 import cv2  # 解决一下vsc报错
import time
import numpy as np

def match_image(image, templ, similarity = 0.8, all = False):
    '''
    image: 需要查找的图像
    templ: 背景
    '''
    try:
        if type(image) == str:
            if not '.' in image:
                image = image + '.jpg'
            # 原本是直接cv2.imread(image) 但是可怜的孤儿opencv不能读取中文名称文件
            image = cv2.imdecode(np.fromfile(image, dtype=np.uint8), -1)
        if type(templ) == str:
            templ = cv2.imdecode(np.fromfile(templ, dtype=np.uint8), -1)
        match_info = cv2.matchTemplate(image,templ,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_info)
        if all == True:
            _xys = []
            for i in range(len(match_info)):
                _tmp = match_info[i]
                _xs = np.where(_tmp > similarity)
                # print(_xs[0])
                for j in _xs[0]:
                    _xys.append((int(j),int(i)))
            return _xys

        # print(match_info[506][34])
        if max_val > similarity:
            position = max_loc
        else:
            position = (-1, -1)
        return position
    except Exception as e:
        print(e)
        return (-1, -1)

def load_img(image):
    try:
        if type(image) == str:
            if not '.' in image:
                image = image + '.jpg'
            # 原本是直接cv2.imread(image) 但是可怜的孤儿opencv不能读取中文名称文件
            return cv2.imdecode(np.fromfile(image, dtype=np.uint8), -1)
    except Exception as e:
        print(e)

        
# 还不能用
def load_img_byte(image):
    try:
        return cv2.imdecode(np.fromiter(image, dtype=np.uint8))
    except Exception as e:
        print(e)

if __name__ == "__main__":
    pos = match_image('0.jpg','1.jpg')
    print(pos)
    pass