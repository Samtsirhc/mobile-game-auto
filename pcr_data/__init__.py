import json
import os
from .unit_manager import UnitManager
from .team_manager import TeamManager
from .tools import load_img

class JJCSearcher:
    def __init__(self):
        self.u = UnitManager()
        self.t = TeamManager()
        self._tmp = '_tmp.jpg'
    
    def search(self, team):
        _team = []
        for i in team:
            i.save(self._tmp)
            _tmp = load_img(self._tmp)
            _team.append(self.u.reg_wife(_tmp))
        return self.t.serch(_team)

