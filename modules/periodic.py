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
        self.log_list = log_list
        self.loop_type = loop_type
        self.init_basic_log(self.log_list)
        self.init()
    
    def init(self):
        self.week = get_week(0, -5*3600)
        self.date = get_time(4, -5*3600)
        if self.loop_type == 1:
            self.log_path = f'{self.dir}{self.name} {self.date}.json'
        elif self.loop_type == 7:
            self.log_path = f'{self.dir}{self.name} {self.week}.json'
        else:
            print('error!!!!!!!!!!!!')
        if os.path.isfile(self.log_path):
            with open(self.log_path, 'rb') as f:
                self.log = json.load(f)
            pass
        else:
            with open(self.log_path, 'w', encoding = 'utf-8') as f:
                f.write(self.basic_log)
            with open(self.log_path, 'rb') as f:
                self.log = json.load(f)
        pass

    def init_basic_log(self, log_list):
        self.basic_log = {}
        for i in log_list:
            self.basic_log[i] = False
        self.basic_log = json.dumps(self.basic_log, ensure_ascii=False)

    def check(self, key):
        self.init()
        return self.log[key]

    def finish(self, key):
        self.init()
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