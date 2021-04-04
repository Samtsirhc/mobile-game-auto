import os
import time


def get_path(layers = 0, mode = 0):
    '''
    layers是层数，往上翻多少层；mode是模式：0返回路径；1返回那个文件夹的名称；
    '''
    if layers == 0:
        tmp = os.getcwd() # 当前目录路径
    else:
        tmp = os.getcwd()
        for _ in range(layers):
            tmp = os.path.dirname(tmp) # 当前目录往上翻i层的目录路径
    if mode == 0:
        return tmp
    if mode == 1:
        for i in range(-len(tmp)+1,0):
            if tmp[-i] == "\\":
                tmp = tmp[-i+1:]
                return tmp

def get_files(path, mode = 0):
    '''
    mode：0，当前目录路径；1，当前目录文件夹；2，当前目录文件
    '''
    for root, dirs, files in os.walk(path):
        if mode == 0:
            return root  
        if mode == 1:
            return dirs  
        if mode == 2:
            return files 

        
if __name__ == '__main__' :
    print(get_files(get_path(),1))
