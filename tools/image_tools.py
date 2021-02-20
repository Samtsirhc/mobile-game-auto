from cv2 import cv2  # 解决一下vsc报错
import time
import numpy as np

def match_image(image, templ, similarity = 0.8):
    try:
        if type(image) == str:
            if not '.jpg' in image:
                image = image + '.jpg'
            # 原本是直接cv2.imread(image) 但是可怜的孤儿opencv不能读取中文名称文件
            image = cv2.imdecode(np.fromfile(image, dtype=np.uint8), -1)
        if type(templ) == str:
            templ = cv2.imdecode(np.fromfile(templ, dtype=np.uint8), -1)
        match_info = cv2.matchTemplate(image,templ,cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_info)
        if max_val > similarity:
            position = max_loc
        else:
            position = (-1, -1)
        return position
    except Exception as e:
        print(e)
        return (-1, -1)


if __name__ == "__main__":
    pos = match_image('啊.jpg','2.jpg')
    print(pos)
    pass