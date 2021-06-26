import string
import time
from datetime import datetime

def get_time(time_structure = 0, diff = 0):

    """ 
    time_structure：
    0. 返回此形式时间 2020-01-16 15:20:20 str
    1. 返回此形式时间 15:20:20 200 最后三位数是毫秒 str
    2. 返回毫秒级时间戳 int
    3. 返回list时间[15, 20, 20, 200] 对应 时，分，秒，毫秒
    4. 返回此形式时间 2020-01-16 str
    5. 返回此形式时间 20200116 str

    diff:
    偏移量，单位是秒
    """
    _now = time.time() + diff
    _struct_time = time.localtime(_now)
    if time_structure == 0:
        _time = time.strftime("%Y-%m-%d %H:%M:%S", _struct_time) 
    if time_structure == 1:
        _time = time.strftime("%H:%M:%S ", _struct_time)
        _time += str(time.time()).split('.')[1][:3]
    if time_structure == 2:
        _time = int(_now * 1000)
    if time_structure == 3:
        _time = [_struct_time.tm_hour,
        _struct_time.tm_min,
        _struct_time.tm_sec,
        int(str(_now).split('.')[1][:3])]
    if time_structure == 4:
        _time = time.strftime("%Y-%m-%d", _struct_time) 
    if time_structure == 5:
        _time = time.strftime("%Y%m%d", _struct_time) 
    return _time        


def get_week(time_structure = 0, diff = 0):
    '''
    0.返回当年的第N周 2021-10 str
    1.返回当年的第N周 [2021, 10] list<int>

    diff:
    偏移量，单位是秒
    """
    '''
    _basic_2021 = 1609689600000
    _difference = get_time(2, diff) - _basic_2021
    _week_count = int(_difference / (7*24*3600*1000)) + 2

    _today = get_time(5)
    _year = get_time().split('-')[0]
    _week_day = datetime.strptime(_today,"%Y%m%d").weekday() + 1
    if time_structure == 0:
        return f'{_year}-{_week_count}'
    if time_structure == 1:
        return [_year, _week_count]

if __name__ == "__main__":
    a = time.time()
    a = time.localtime(a)
    print(a)
