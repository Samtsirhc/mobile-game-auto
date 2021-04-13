import os
import sys

PKGS = [{'module': 'uiautomator2', 'package': 'uiautomator2', 'version':'2.12.1'},
        {'module': 'psutil', 'package': 'psutil', 'version':'5.8.0'},
        {'module': 'cv2', 'package': 'opencv-python', 'version':'4.2.0.34'},
        {'module': 'adbutils', 'package': 'adbutils', 'version':'0.10.0'},
        {'module': 'websocket', 'package': 'websocket_client', 'version':'0.58.0'},
        {'module': 'pillow', 'package': 'pillow', 'version':'8.0.1'}]

def check_environment(pkgs):
    print('checking...')
    for i in pkgs:
        try:
            exec(f'import {i["module"]}')
            print(f'{i["module"]}')
        except:
            os.system(f'pip install {i["package"]}=={i["version"]}')
            check_environment(pkgs)
            break
    else:
        print('Environment Done!')

check_environment(PKGS)
os.system('pause')
