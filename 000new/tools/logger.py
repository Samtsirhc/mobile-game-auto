import logging
import time
from logging.handlers import HTTPHandler
import requests
import string

def creat_my_logger(logger_name = "MyLogger", log_path = "", log_file_name = ""):
    # 记录器，在这里设置一个最低级的level，那么在处理器中再设置高级的就能起效，反之会无效
    logger = logging.getLogger(logger_name)

    # 控制台处理器，这里又设置了等级，表示这个实例的控制台处理器打出的等级大于等于这个
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # 写入文件的日志处理器
    _time = time.strftime("%Y-%m-%d", time.localtime())
    if log_file_name == "":
        pass
    else:
        _time += " "
    fileHandler = logging.FileHandler(filename = f'{log_path}{_time}{log_file_name}.log')
    fileHandler.setLevel(logging.INFO)

    # 设定格式
    formatter = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s] [%(filename)s] [%(lineno)s]: %(message)s',
                                datefmt='%H:%M:%S')    # datefmt='%Y-%m-%d %H:%M:%S'

    # 给处理器们设置格式
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 给记录器添加处理器
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    # 设定一个过滤器
    flt = logging.Filter(logger_name)
    logger.addFilter(flt)
    return logger

class Logger():
    def __init__(self,logger_name = "MyLogger", log_path = "", log_file_name = "", cq_config =''):
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(logging.INFO)
        self.cq_config = cq_config
        if len(self._logger.handlers) > 0:
            return
        self.get_format()
        self.add_console_handler()
        self.add_file_handler(log_path = log_path, log_file_name = log_file_name)
        self.set_flt(logger_name)
        pass

    def add_console_handler(self, level = logging.DEBUG):
        _consoleHandler = logging.StreamHandler()
        _consoleHandler.setLevel(level)
        _consoleHandler.setFormatter(self.fmt)
        self.add_handler(_consoleHandler)

    def add_file_handler(self, level = logging.DEBUG, log_path = "", log_file_name = ""):
        _time = time.strftime("%Y-%m-%d", time.localtime())
        if log_file_name == "":
            pass
        else:
            _time += " "
        _fileHandler = logging.FileHandler(filename = f'{log_path}{_time}{log_file_name}.log')
        _fileHandler.setLevel(level)
        _fileHandler.setFormatter(self.fmt)
        self.add_handler(_fileHandler)

    def add_handler(self, handler):
        self._logger.addHandler(handler)
    
    def get_format(self):
        self.fmt = logging.Formatter(fmt='[%(asctime)s] [%(levelname)s]: %(message)s',
                                datefmt='%H:%M:%S')    # datefmt='%Y-%m-%d %H:%M:%S'
    def set_flt(self, logger_name):
        flt = logging.Filter(logger_name)
        self._logger.addFilter(flt)

    def get_logger(self):
        return self
    
    def debug(self, msg):
        self._logger.debug(msg)

    def info(self, msg):
        self._logger.info(msg)
        try:
            requests.get(self.cq_config.replace('MSG', msg))
        except:
            print('your qbot is off-line')
    
    def error(self, msg):
        self._logger.error(msg)
        try:
            requests.get(self.cq_config.replace('MSG', msg))
        except:
            print('your qbot is off-line')
    
    def setLevel(self, level):
        self._logger.setLevel(level)

if __name__ == "__main__":
    # send_private_msg?user_id=QQ_NUMBER&message=MSG?
    tmp = Logger()
    tmp = tmp.get_logger()
    tmp.setLevel(logging.DEBUG)
    tmp.info(1)
    pass