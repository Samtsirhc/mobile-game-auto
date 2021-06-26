from tools import count_list, get_time, list2str, load_json, write_json, load_img
from unit import id2name, name2id
import requests
import json
import os
player_data_path = 'team_data/player_data'
player_imgs_path = 'team_data/player_imgs'

class PlayerManager:
    def __init__(self):

        pass
    
    def load_player(self):
        self.players = os.listdir(player_data_path)
        self.player_data = {}
        self.player_imgs = {}
        for i in self.players:
            self.player_data[i.replace('.json', '')] = load_json(player_data_path + '/' + i)
            self.player_data[i.replace('.json', '')] = load_img(player_imgs_path + '/' + i.replace('json', 'jpg'))

    
    def creat_player(self, player, team):
        _time = get_time()
        player.save(player_imgs_path + '/' + _time + '.jpg')
        _unknow = 0




    def search_player(self, player):
        pass
if __name__ == "__main__":
# 好像是费力不讨好，算了
    pass
