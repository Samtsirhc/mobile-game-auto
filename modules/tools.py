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
    
def list_combinate(my_list, N, n):
        '''
        输入N = n
        my_list要是list
        长度大于等于N
        '''
        _res = []
        if n == N:
            _my_list = [[i] for i in my_list]
        else:
            _my_list = my_list
        lens = len(_my_list)
        if n < 0 or type(n) != int:
            raise ValueError
        if n == 1 or lens < n:
            return _my_list
        else:
            for i in range(lens - n + 1):
                _list = list_combinate(_my_list[i+1:], N, n-1)
                for j in _list:
                    _res.append(j + _my_list[i])
        return _res
if __name__ == "__main__":
    a = [[1,2,3],[1,2,4],[23,4],'aaa']
    count = 3
    print(list_combinate(a,count,count))

