import json
import os

def format_json(file):
    _tmp = None
    with open(file, 'rb') as f:
        _tmp = json.loads(f.read())
    with open(file, 'w', encoding='utf-8') as f:
        f.write(json.dumps(_tmp, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))
    
if __name__ == "__main__":
    res = os.walk(os.getcwd())
    for root, dirs, files in res:
        for i in files:
            if '.json' in i:
                format_json(i)
