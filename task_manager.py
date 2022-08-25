import ctypes
import inspect
import time
from threading import Thread
import os

from modules.process_tool import close_process
from modules.tools import load_json
from emulator import Emulator


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    try:
        _async_raise(thread.ident, SystemExit)
    except Exception as e:
        pass


class TaskManager():
    def __init__(self):
        self.load_config()
        self.threads = []

    def stop_all(self):
        try:
            for i in self.threads:
                stop_thread(i)
            self.close_emu()
            time.sleep(3)
            self.threads = []
            e = Emulator()
            e.connect()
            return f'已经停止 {str(i)}'
        except Exception as e:
            return str(e)

    def load_config(self):
        self.pcr = load_json('config/pcr.json')
        self.arknights = load_json('config/arknights.json')

    def close_emu(self):
        close_process('Nox.exe')

    def run_task(self, task):
        _task = None
        try:
            task_type, task_name = task.split(' ')
            self.stop_all()
            if task_type == '方舟':
                # _task = self.arknights[task_name]
                # from arknights_scripts import ark_run
                def ark():
                    os.system('%ARK_AUTO%')
                    pass
                _thread = Thread(target=ark)
            else:
                _task = self.pcr[task_name]
                from pcr_scripts import pcr_run
                _thread = Thread(target=pcr_run, args=(_task,))
            _thread.start()
            self.threads.append(_thread)
            return '成功'
        except Exception as e:
            return str(e)


if __name__ == "__main__":
    # t = TaskManager()
    # t.run_task('方舟 日常刷石头')
    # time.sleep(60)
    # t.stop_all()
    os.system('%ARK_AUTO%')
