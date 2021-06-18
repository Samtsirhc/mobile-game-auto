import json
import os
from c_name import WIFES_NAME

with open('unita.json', 'rb') as f:
    a = json.load(f)
b = WIFES_NAME
c = {}

for i in a:
    _id = i['id']
    _name = i['name']
    for j in WIFES_NAME:
        if WIFES_NAME[j][1] == _name:
            c[int(_id)] = WIFES_NAME[j]
            print(WIFES_NAME[j])
with open('unit_data.json', 'w', encoding = 'utf-8') as f:
    f.write(json.dumps(c, ensure_ascii=False))

os.system('pause')