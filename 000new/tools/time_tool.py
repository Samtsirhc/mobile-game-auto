import string
import time

def get_time(time_structure = 0):

    """ 
    time_structure：
    0. 返回此形式时间 2020-01-16 15:20:20 str
    1. 返回此形式时间 15:20:20 200 最后三位数是毫秒 str
    2. 返回毫秒级时间戳 int
    3. 返回list时间[15, 20, 20, 200] 对应 时，分，秒，毫秒
    4. 返回此形式时间 2020-01-16 str
    """
    if time_structure == 0:
        _time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    if time_structure == 1:
        _time = time.strftime("%H:%M:%S ", time.localtime())
        _time += str(time.time()).split('.')[1][:3]
    if time_structure == 2:
        _time = int(time.time() * 1000)
    if time_structure == 3:
        _time = [time.localtime().tm_hour,
        time.localtime().tm_min,
        time.localtime().tm_sec,
        int(str(time.time()).split('.')[1][:3])]
    if time_structure == 4:
        _time = time.strftime("%Y-%m-%d", time.localtime()) 
    return _time        

if __name__ == "__main__":
    for _ in range(10):
        time.sleep(0.5)
        print(get_time(3))
    pass
