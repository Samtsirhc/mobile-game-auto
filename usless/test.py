import sys

def a():
    print(sys._getframe().f_code.co_name)

def b():
    print(sys._getframe().f_code.co_name)

def c():
    print(sys._getframe().f_code.co_name)

def run_tasks(tasks):
    for i in tasks:
        exec(f'{i}()')