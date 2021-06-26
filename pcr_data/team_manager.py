from pcr_data.tools import load_json, write_json, list2str, get_time
import requests
import json
from pcr_data.team import Team
import os


unget_roles_file = os.path.dirname(__file__) + '/team_data/unget_roles.json'
pjjc_data_file = os.path.dirname(__file__) + '/team_data/pjjc_atk.json'


class TeamManager:
    def __init__(self):
        self.init_unget_role()
        self.init_pjjc_atk()
        pass

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
        del _team
        return _solutions


if __name__ == "__main__":
    a = TeamManager()
