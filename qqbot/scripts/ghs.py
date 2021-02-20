import requests
import sys
ip = '127.0.0.1'
port = 5700

def send_private_msg(user_id, message):
    func_name = sys._getframe().f_code.co_name
    echo = requests.request("GET",f"http://{ip}:{port}/{func_name}?user_id={user_id}&message={message}")
    return echo

def send_group_msg(group_id, message):
    func_name = sys._getframe().f_code.co_name
    echo = requests.request("GET",f"http://{ip}:{port}/{func_name}?group_id={group_id}&message={message}")
    return echo

def get_msg(message_id):
    func_name = sys._getframe().f_code.co_name
    echo = requests.get(f"http://{ip}:{port}/{func_name}?message_id={message_id}")
    echo = echo.content.decode()
    return echo

a = get_msg('1925855109')

print(a)