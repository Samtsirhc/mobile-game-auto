import json
import os

def delet(file):
    _tmp = None
    with open(file, 'rb') as f:
        _tmp = json.loads(f.read())
        if len(_tmp['solutions']) < 2:
            _tmp = 0
    if _tmp == 0:
        os.remove(file)
    
if __name__ == "__main__":
    res = os.walk(os.getcwd())
    for root, dirs, files in res:
        for i in files:
            if '.json' in i:
                delet(i)
