from tools import count_list, get_time, list2str
from unit import id2name, name2id
import requests
import json


class Team:
    def __init__(self, team):
        if type(team) == list:
            self.data = {"team_id":[], "team_name":[], "solutions":[]}
            self.team_name = []
            self.init_team(team)
        else:
            self.data = team
            self.name = list2str(self.data["team_id"])

    def init_team(self, team):
        if '1' in team[0] or '2' in team[0]:
            self.data["team_id"] = team
        else:
            self.data["team_id"] = [name2id(i) for i in team]
        self.data["team_id"].sort()
        self.data["team_name"] = [id2name(i) for i in self.data["team_id"]]
    
    def format2dict(self):
        _dict = {}
        _dict[self.name] = self.data
        return _dict


class JJCDef(Team):
    def __init__(self, team: list):
        Team.__init__(self, team)
        self.init_serch()
        self.get_solutions()
        self.data["record_time"] = get_time()
        self.on_def_record = {"win":[], "lose":[], "rate":1, "rate_14":1}
        self.format = self.format2dict()

    def init_serch(self):
        self.search_url = r"https://server.whitemagic2014.com/pcrjjc/api/temp"
        self.headers = {"authorization": '720828494',
                        'User-Agent': 'PostmanRuntime/7.28.0', 'content-type': 'application/json'}
        self.payload = {"def": [], "region": 3}

    def get_solutions(self):
        _solutions = self.serch_in_net([int(i) for i in self.data["team_id"]])
        if len(_solutions) > 3:
            _solutions = _solutions[:3]
        self.solutions = []
        for i in _solutions:
            _tmp = []
            for j in i:
                _tmp.append(id2name(j))
            self.data["solutions"].append(_tmp)


    def serch_in_net(self, team):
        self.payload['def'] = team
        _re = requests.post(self.search_url, data=json.dumps(
            self.payload), headers=self.headers)
        _re = json.loads(_re.text)
        try:
            _row_data = _re['data']['result']
        except:
            return [self.data["team_id"]]
        _teams = []
        for i in _row_data:
            _tmp = []
            for j in i['atk']:
                _tmp.append(j['id'])
            _teams.append(_tmp)
        return _teams

class PJJCDef():
    def __init__(self, teams, player):
        self.teams = teams
        self.player = player
        pass

    def 

if __name__ == "__main__":
    a = {'a': 1}
    b = {'a': 2, 'b': 2}
    a = dict(b, **a)
    print(a)
