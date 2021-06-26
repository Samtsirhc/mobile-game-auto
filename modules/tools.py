import json
import os
import time
import numpy as np
from cv2 import cv2

def img_resize(*args):
    return cv2.resize(*args)

# from modules.image_tool
def load_img(image):
    try:
        if type(image) == str:
            if not '.' in image:
                image = image + '.jpg'
            # 原本是直接cv2.imread(image) 但是可怜的孤儿opencv不能读取中文名称文件
            return cv2.imdecode(np.fromfile(image, dtype=np.uint8), -1)
    except Exception as e:
        print(e)

# from modules.image_tool
def match_image(image, templ, similarity = 0.8):
    '''
    image: 需要查找的图像
    templ: 背景
    '''

    match_info = cv2.matchTemplate(image,templ,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_info)
    if max_val > similarity:
        return max_val
    else:
        return max_val

def load_json(file) -> dict:
    with open(file, 'rb') as f:
        return json.loads(f.read())


def write_json(file, data: dict):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))

def count_list(my_list, minist):
    _tmp = 0
    for i in my_list:
        if i > minist:
            _tmp += 1
    return _tmp
    
def get_time():
    return time.time()

def list2str(my_list):
    _tmp = ''
    for i in my_list:
        _tmp += str(i)
    return _tmp

def get_all_files_name(path):
    # os.path.dirname(__file__) + '/' + 
    pass
    
if __name__ == "__main__":
    a = {'1':2}
    write_json('/1.json', a)
    pass

