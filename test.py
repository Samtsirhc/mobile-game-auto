import json

FILE_NAME = 'tasks.json'

def write_task(task_name, script_name, tasks):
    _data = None
    with open(FILE_NAME, 'rb') as f:
        _data = json.loads(f.read())
    _data[task_name]['script_name'] = script_name
    _data[task_name]['tasks'] = tasks

    with open(FILE_NAME, 'w', encoding='utf-8') as f:
        f.write(json.dumps(_data, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))


if __name__ == '__main__':
    task_name = "arknights_daily"
    script_name = "arknights_scripts.py"
    tasks = ['1','2']
    write_task(task_name, script_name, tasks)

 

