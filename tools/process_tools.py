from cv2 import cv2  # 解决一下vsc报错
import time
import numpy as np
import psutil
import os

#运行某程序
def run_sth(FileName,RunType = 1,FilePath = ""):
    if RunType == 0:
        CurrentPath = os.getcwd() + "\\" + FileName
        if os.path.isfile(CurrentPath):
            print ("目标==> " + FileName +" <==在当前目录")
            os.system("start " + CurrentPath)      #不加start会阻塞
        else:
            UpperPath = os.path.dirname(os.getcwd()) + "\\" + FileName 
            if os.path.isfile(UpperPath):
                print ("目标==> " + FileName +" <==在上层目录")
                os.system("start " + UpperPath)     #不加start会阻塞
            else:
                print("找不到目标：" + FileName)
    if RunType == 1:
        FilePath = FileName 
        os.system("start " + FilePath)     #不加start会阻塞
        print ("已经运行：" + FileName)

def run(path):
    os.system("start " + path)     #不加start会阻塞
    print ("已经运行：" + path)

def check_process(name):
    pl = psutil.pids()
    for pid in pl:
        try:
            if psutil.Process(pid).name() == name:
                print(f'{name} has been running')
                return True
        except:
            pass    
    return False
#关闭某进程
def close_process(Name):
    ExePath = "taskkill /IM " + Name + " /F"
    os.system(ExePath)