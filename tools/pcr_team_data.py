import json
import requests

class TeamData:
    def __init__(self, unit_data_path, team_data_path):
        self.unit_data_path = unit_data_path
        self.unit_data = None
        self.team_data_path = team_data_path
        self.team_data = {}

        self.search_url = r"https://server.whitemagic2014.com/pcrjjc/api/temp"
        self.headers = {"authorization":'720828494', 'User-Agent':'PostmanRuntime/7.28.0','content-type': 'application/json'}
        self.payload = {"def":[105201,103401,101001,100201,101801], "region":3}

        self.load_team_data()
        self.load_unit_data()
        pass

    def load_unit_data(self):
        with open(self.unit_data_path, 'r', encoding='utf-8') as f:
            self.unit_data = json.loads(f.read())

    def load_team_data(self):
        with open(self.team_data_path, 'r', encoding='utf-8') as f:
            self.team_data = json.dumps(f.read())

    def search(self, team):
        _team = []
        for i in team:
            _id = 000000
            if type(i) == int:
                _id = i
            else:
                _id = self.name2id(i)
            _team.append(_id)
        _res_id = self.search_in_local(_team[0])
        _res_name = []
        for i in _res_id['team']:
            _res_name.append(self.id2name(i))
        return _res_name
                
    
    def search_in_local(self, team):
        team.sort()
        _key_name = self.list2int(team)
        if _key_name not in self.team_data:
            self.search_in_net(team)
        return self.team_data[_key_name]
        
    def search_in_net(self, team):
        team.sort()
        self.payload['def'] = team
        _re = requests.post(self.search_url, data=json.dumps(self.payload), headers=self.headers)
        _re =json.loads(_re.text)
        _row_data = _re['data']['result']
        _teams = []
        for i in _row_data:
            _tmp = []
            for j in i['atk']:
                _tmp.append(j['id'])
            _teams.append({'team':_tmp, 'win':0, 'lose':0 })
        _key_name = self.list2int(team)
        self.team_data[_key_name] = _teams
        with open(self.team_data_path, 'w', encoding= 'utf-8') as f:
            _tmp = json.dumps(self.team_data, ensure_ascii= False)
            f.write(_tmp)
        
    
    def list2int(self, the_list):
        _tmp = ''
        for i in the_list:
            if type(i) != int:
                raise TypeError
            _tmp += str(i)
        return _tmp

    def name2id(self, name):
        for i in self.unit_data:
            if name in self.unit_data[i]:
                return int(i)
        else:
            raise KeyError
    
    def id2name(self, id):
        id = str(id)
        return self.unit_data[id]



if __name__ == "__main__":
    a = {1:222,2:2}
    a = json.dumps(a)
    a = json.loads(a)
    print(a)

