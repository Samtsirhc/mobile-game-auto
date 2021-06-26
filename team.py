
import json
import os

import requests
from modules.tools import *
from unit import id2name, name2id

solution_path = "pcr_data/team_data/solutions/"


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
            if get_time() - self.data['record_time'] > 30 * 24 * 3600:
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
        _re = requests.post(self.search_url, data=json.dumps(self.payload), headers=self.headers)
        _re = json.loads(_re.text)
        try:
            _row_data = _re['data']['result']
        except:
            return [self.ids]
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
    
    def check_unget(self, team):
        for i in self.unget_roles:
            if i in team:
                return False
        return True
        
    def init_unget_role(self):
        self.unget_roles = load_json(unget_roles_file)['unget_roles']

    def write_pjjc_data(self):
        sorted(self.pjjc_atk, key=lambda i: i['rate'])
        write_json(pjjc_data_file, {'data': self.pjjc_atk})

    def report_pjjc_result(self, team, result):
        _team = Team(team)
        _time = get_time()
        for i in self.pjjc_atk:
            if i['name'] == _team.name:
                i['total'].append(_time)
                if result:
                    i['win'].append(_time)
                break
        self.write_pjjc_data()

    def init_pjjc_atk(self):
        self.pjjc_atk = load_json(pjjc_data_file)['data']
        _now = get_time()
        _ddl_time = _now - 14 * 24 * 3600
        for i in self.pjjc_atk:
            if len(i.keys()) == 1:
                _team = Team(i['team'])
                i['name'] = _team.name
                i['total'] = [_now, _now, _now]
                i['win'] = [_now, _now, _now]
            # else:
            #     _keys = ['total', 'win', 'lose']
            #     for j in _keys:
            #         for k in range(len(i[j])):
            #             if i[j][k] < _ddl_time:
            #                 i[j][k].remove()
            i['rate'] = round(len(i['win'])/len(i['total']), 3)
        self.write_pjjc_data()

    def serch(self, team):
        _team = Team(team)
        _solutions = _team.get_solutions()
        return _solutions


if __name__ == "__main__":
    a = Team(["羊驼", "酒鬼", "ue", "露娜", "星法"])
    c = a.get_solutions()
    print(c)
    pass
