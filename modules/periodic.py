import json
import os
if __name__ == "__main__":
    from time_tool import get_time, get_week
else:
    from modules.time_tool import get_time, get_week

class Periodic():
    def __init__(self, log_list, name, loop_type, log_dir):
        '''
        log_list：循环的任务列表
        name：任务组的名称
        loop_type：循环的类型。1，日循环；7，周循环
        '''
        self.name = name
        self.dir = log_dir
        self.init_basic_log(log_list)
        self.set_loop_type(loop_type)
        self.check_log()
        
    def init_basic_log(self, log_list):
        self.basic_log = {}
        for i in log_list:
            self.basic_log[i] = False
        self.basic_log = json.dumps(self.basic_log, ensure_ascii=False)

    def check_log(self):
        if os.path.isfile(self.log_path):
            with open(self.log_path, 'rb') as f:
                self.log = json.load(f)
            pass
        else:
            with open(self.log_path, 'w', encoding = 'utf-8') as f:
                f.write(self.basic_log)
            with open(self.log_path, 'rb') as f:
                self.log = json.load(f)

    def set_loop_type(self, loop_type):
        if get_time(3)[0] > 5:
            self.week = get_week()
            self.date = get_time(4)
        else:
            self.week = get_week(0, 24*3600)
            self.date = get_time(4, 24*3600)
        if loop_type == 1:
            self.log_path = f'{self.dir}{self.name} {self.date}.json'
        elif loop_type == 7:
            self.log_path = f'{self.dir}{self.name} {self.week}.json'
        else:
            print('error!!!!!!!!!!!!')
    
    def check(self, key):
        self.check_log()
        return self.log[key]

    def finish(self, key):
        with open(self.log_path, 'rb') as f:
            self.log = json.load(f)
            self.log[key] = True
        with open(self.log_path, 'w', encoding = 'utf-8') as f:
            f.write(json.dumps(self.log, ensure_ascii=False))

    def periodic_manager(self, func):
        def dec():
            if self.check(func.__name__):
                pass
            else:
                func()
        return dec

if __name__ == "__main__":
    pass