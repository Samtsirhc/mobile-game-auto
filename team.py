
import json
import os

import requests

from config import get_logger
from modules.tools import *
from modules.tools import list_combinate as lc
from unit import id2name, name2id, nick_name2name, UNIT_DATA
import random

solution_path = "pcr_data/team_data/solutions/"
l = get_logger()


class Team:
    def __init__(self, team):
        self.init_team(team)
        self.init_serch()
        pass

    def init_team(self, team):
        self.ids = []
        for i in team:
            if '1' not in i and '2' not in i and type(i) != int:
                self.ids.append(name2id(i))
            else:
                self.ids.append(str(i))
        self.ids.sort()
        self.names = [id2name(i) for i in self.ids]
        self.name = list2str(self.ids)

    def init_serch(self):
        self.search_url = r"https://server.whitemagic2014.com/pcrjjc/api/temp"
        self.headers = {"authorization": '720828494',
                        'User-Agent': 'PostmanRuntime/7.28.0', 'content-type': 'application/json'}
        self.payload = {"def": [], "region": 3}

    def get_solutions(self):
        _file_name = f'{solution_path}{self.name}.json'
        try:
            self.data = load_json(_file_name)
            if get_time() - self.data['record_time'] > 30 * 24 * 3600 or len(self.data['solutions']) < 2:
                raise KeyError
        except:
            _solutions = self.serch_in_net([int(i) for i in self.ids])
            self.data = {'record_time': 0, 'solutions': []}
            self.data['record_time'] = get_time()
            for i in _solutions:
                _tmp = []
                for j in i:
                    _tmp.append(id2name(j))
                self.data["solutions"].append(_tmp)
            write_json(_file_name, self.data)
        return self.data["solutions"]

    def serch_in_net(self, team):
        self.payload['def'] = team
        _re = requests.post(self.search_url, data=json.dumps(
            self.payload), headers=self.headers)
        _re = json.loads(_re.text)
        try:
            _row_data = _re['data']['result']
        except:
            l.info(_re)
            return []
        _teams = []
        for i in _row_data:
            _tmp = []
            for j in i['atk']:
                _tmp.append(j['id'])
            _teams.append(_tmp)
        return _teams


unget_roles_file = 'pcr_data/team_data/unget_roles.json'
pjjc_data_file = 'pcr_data//team_data/pjjc_atk.json'


class TeamManager:
    def __init__(self):
        self.init_unget_role()
        self.init_pjjc_atk()
        pass

    def check_unget(self, team, used=None):
        if used == None:
            used = self.unget_roles
        for i in used:
            if i in team:
                return False
        return True

    def role_available(self, roles):
        if type(roles) == list:
            _tmp = roles + self.unget_roles
            if len(set(_tmp)) == len(_tmp):
                return True
            else:
                return False
        else:
            if roles in self.unget_roles:
                return False
            else:
                return True

    def init_unget_role(self):
        self.unget_roles = load_json(unget_roles_file)['unget_roles']
        for i in range(len(self.unget_roles)):
            self.unget_roles[i] = nick_name2name(self.unget_roles[i])
        write_json(unget_roles_file, {'unget_roles': self.unget_roles})

    def write_pjjc_data(self):
        self.pjjc_atk = sorted(self.pjjc_atk, key=lambda i: i['rate'], reverse=True)
        write_json(pjjc_data_file, {'data': self.pjjc_atk})

    def report_pjjc_result(self, team, result):
        _team = Team(team)
        _time = get_time()
        for i in self.pjjc_atk:
            if i['name'] == _team.name:
                i['total'].append(_time)
                if result:
                    i['win'].append(_time)
                i['rate'] = round(len(i['win'])/len(i['total']), 3)
                self.write_pjjc_data()
                l.info(f'更新结果 {team} {result}')
                break
        else:
            l.info(f'结果未记录 {team} {result}')


    def init_pjjc_atk(self):
        self.pjjc_atk_record_time = os.path.getmtime(pjjc_data_file)
        self.pjjc_atk = load_json(pjjc_data_file)['data']
        _now = get_time()
        _ddl_time = _now - 14 * 24 * 3600
        _re = []
        for i in self.pjjc_atk:
            try:
                _re.append(i['name'])
            except:
                pass
        for i in self.pjjc_atk:
            if len(i.keys()) == 1:
                _team = Team(i['team'])
                i['name'] = _team.name
                i['team'] = _team.names
                i['total'] = [_now, _now, _now]
                i['win'] = [_now, _now, _now]
                if i['name'] in _re or '未知' in i['team']:
                    l.info(f'移除了 {i["team"]}')
                    self.pjjc_atk.remove(i)
                else:
                    i['rate'] = round(len(i['win'])/len(i['total']), 3)
                    l.info(f'初始化了 {i["team"]}')
        self.write_pjjc_data()

    def serch(self, team):
        _team = Team(team)
        _solutions = _team.get_solutions()
        return _solutions

    def get_best_teams(self, used, count):
        def get_unused_teams(teams, used):
            _teams = []
            for i in self.pjjc_atk:
                for j in used:
                    if j in i['team']:
                        break
                else:
                    _teams.append(i.copy())
            return _teams

        def get_conflict_free_teams(teams, used, count):
            _teams = get_unused_teams(teams, used)
            _teams_combinate = lc(_teams, count, count)
            _free_teams = []
            for i in _teams_combinate:
                _tmp_list = []
                for j in i:
                    _tmp_list += j['team']
                if len(set(_tmp_list)) != count * 5:
                    continue
                _tmp_dict = {'teams': [], 'rate': 0}
                for j in i:
                    _tmp_dict['teams'].append(j['team'])
                    _tmp_dict['rate'] += j['rate']
                _free_teams.append(_tmp_dict)
            return _free_teams

        def add_role(used):
            _role = None
            _key = random.sample(UNIT_DATA.keys(), 1)[0]
            if UNIT_DATA[_key][0] in used:
                _role = add_role(used)
            else:
                _role = UNIT_DATA[_key][0]
            return _role


        _safe_teams = get_unused_teams(self.pjjc_atk, self.unget_roles)
        _safe_team_group = get_conflict_free_teams(_safe_teams, used, count)
        if _safe_team_group == []:
            _teams = self.get_best_teams(used, count - 1)
            for i in _teams:
                used += i
            _tmp = []
            for _ in range(5):
                _role = add_role(used)
                used += _role
                _tmp.append(_role)
            _teams.append(_tmp)
            return _teams
        else:
            _safe_team_group = sorted(_safe_team_group, key=lambda i: i['rate'], reverse=True)
            return (_safe_team_group[0]['teams'], _safe_team_group[0]['rate'])

if __name__ == "__main__":
    a = TeamManager()
    a.write_pjjc_data()

