
import logging
from os import system
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

from modules.process_tool import close_process
from modules.tools import load_json, write_json
from task_manager import TaskManager
from config import get_logger
from team import TeamManager


logger = get_logger()
t = TaskManager()

STOP_COMMAND = ['停止', '停止脚本']
RESTART_COMMAND = ['重启', '重启模拟器', '关闭']
ADD_TEAM_COMMAND = ['添加', '增加']
JJC_COMMAND = ['怎么拆', 'jjc查询']
SET_ARK_COMMAND = ['设置方舟']
RESTART_PC_COMMAND = ['重启电脑']

pcr_atk_path = 'pcr_data/team_data/pjjc_atk.json'
ark_set_path = 'config/Arknights.json'
tm = TeamManager()

def handle_task(task):
    if task.startswith(JJC_COMMAND[0]) or task.startswith(JJC_COMMAND[1]):
        _team = []
        _team = task.split(' ')
        _team.pop(0)
        if len(_team) != 5:
            return '人数不足5或命令错误，示例：jjc查询 角色1 角色2 角色3 角色4 角色5，输入查询不到的角色或无答案的阵容将返回空'
        _teams = tm.serch(_team)
        _res = ''
        for i in _teams:
            _res += str(i) + '\n'
    elif task in STOP_COMMAND:
        _res = t.stop_all()
    elif task in RESTART_COMMAND:
        _res = t.stop_all() + '\n'
        _res += close_process('Nox.exe')
    elif task.startswith(ADD_TEAM_COMMAND[0]) or task.startswith(ADD_TEAM_COMMAND[1]):
        _team = task.split(' ')
        _team.remove(_team[0])
        if len(_team) != 5:
            return '添加失败'
        _json = load_json(pcr_atk_path)
        _json['data'].append({'team':_team})
        write_json(pcr_atk_path, _json)
        _res = '添加了: ' + str(_team)
    elif task.startswith(SET_ARK_COMMAND[0]):
        _json = load_json(ark_set_path)
        _json['当前任务'] = task.split(' ')[1]
        write_json(ark_set_path, _json)
    elif task in RESTART_PC_COMMAND:
        system("shutdown -r -t 100")
    else:
        _res = t.run_task(task)
    return _res


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self.do_HEAD()
        logger.info("GET request received!")
        self.wfile.write("GET request received!".encode('utf-8'))

    def do_POST(self):
        # Get the size of data
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)  # Get the data
        data = post_data.decode('utf-8')
        # logger.info(f"[POST] " + data)
        self.do_HEAD()

        # 处理命令
        _res = handle_task(data)

        self.wfile.write(_res.encode('utf-8'))

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
           <html><head><title>Title goes here.</title></head>
           <body><p>This is a test.</p>
           <p>You accessed path: {}</p>
           </body></html>
           '''.format(path)
        return bytes(content, 'UTF-8')


def run(server_class=HTTPServer, handler_class=Handler, port=8888):
    server_address = ('localhost', port)
    server = server_class(server_address, handler_class)
    logger.info('Http server 已经启动')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logger.info('Http server 已经停止')


if __name__ == '__main__':
    run()


