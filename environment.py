import os
import sys

modules = ['uiautomator2', 'psutil', 'cv2']
packages = ['uiautomator2', 'psutil', 'opencv-python']


for i in range(len(packages)):
    try:
        exec(f'import {modules[i]}')
    except:
        os.system(f'pip install {packages[i]}')
else:
    print('环境已准备好')

os.system('pause')