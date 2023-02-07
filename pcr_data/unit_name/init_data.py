# pip install opencc-python-reimplemented
# pip install pandas pymysql
# pip install cryptography

import os
import string
from _pcr_data import CHARA_NAME
from opencc import OpenCC
import json

# t2s = OpenCC('t2s') # 繁体转简体
# s2t = OpenCC('s2t') # 简体转繁体
# mix2t = OpenCC('mix2t') # 混合体转繁体
# mix2s = OpenCC('mix2s') # 混合体转简体

# for i in CHARA_NAME:
#     _tmp = CHARA_NAME[i][0]
#     print(f'{_tmp} {s2t.convert(_tmp)}')


def extarct_str(mystr, a, b):
    _pos_a = mystr.find(a) + len(a)
    _pos_b = mystr.find(b)
    return mystr[_pos_a: _pos_b]

def get_id_jpname():
    sql_file = 'unit_profile.sql'
    sql = open(sql_file, 'r', encoding = 'utf8')
    sqltxt = sql.readlines()
    sql.close()
    _dict = {}
    for i in sqltxt:
        _tmp1 = extarct_str(i, '/*unit_id*/', ',')
        _tmp2 = extarct_str(i, '/*unit_name*/"', '",')
        _dict[_tmp1] = _tmp2
    return _dict


if __name__ == "__main__":
    # 简体名称转繁体
    s2t = OpenCC('s2t')

    # 这是_pcr_data里面的id 人为修复一些错误 多人角色都有问题 手动修复一下
    corrections = { 'ぺコリーヌ(ニューイヤー)':1118,
                    'ミフユ(作業服)':1167,
                    'ぺコリーヌ(プリンセス)':1804,
                    "アキノ＆サレン":1217,
                    "ハツネ＆シオリ":1807,
                    "ミソギ＆ミミ＆キョウカ":1808
                }
    # 这是游戏里面的id
    extra_nickname = {
        "180901":["秋乃&咲戀"],
        "123001":["爱梅斯"],
        "118501":["花凛"], 
    }
    id_name = {}
    miss = ''
    id_jpname = get_id_jpname()
    for i in id_jpname:
        _name = id_jpname[i]
        _name = _name.replace(' ','')
        _name = _name.replace('（','(')
        _name = _name.replace('）',')')
        _name = _name.replace('&','＆')
        for j in CHARA_NAME:
            if _name in CHARA_NAME[j]:
                id_name[i] = CHARA_NAME[j]
                id_name[i][0] = s2t.convert(id_name[i][0])
                print(id_name[i])
                break
        else:
            for j in corrections:
                if _name == j:
                    id_name[i] = CHARA_NAME[corrections[j]]
                    id_name[i][0] = s2t.convert(id_name[i][0])
                    print(id_name[i])
                    break
            else:
                miss += _name
                miss += '\n'
            pass
    for i in extra_nickname:
        for j in extra_nickname[i]:
            id_name[i].append(j)
        print("额外昵称增加：" + extra_nickname[i][0])

    # 修正一些字错误
    words = [['憐', '怜'], ['裏', '里'], ['喫', '吃']]
    for i in id_name:
        for j in range(len(id_name[i])):
            for k in range(len(words)):
                id_name[i][j] = id_name[i][j].replace(words[k][0], words[k][1])

    print(f'一共有{len(id_name)}个角色')
 
    with open('unit_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(id_name, ensure_ascii=False, sort_keys=True, indent=4, separators=(',', ':')))

    with open('miss.log', 'w', encoding='utf-8') as f:
        f.write(miss) 

    os.system('pause')
    pass



