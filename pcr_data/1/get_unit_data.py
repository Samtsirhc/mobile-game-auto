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

    corrections = { 'ぺコリーヌ(ニューイヤー)':1118,
                    'ミフユ(作業服)':1167,
                    'ぺコリーヌ(プリンセス)':1804}

    id_name = {}
    miss = ''
    id_jpname = get_id_jpname()
    for i in id_jpname:
        _name = id_jpname[i]
        _name = _name.replace(' ','')
        _name = _name.replace('（','(')
        _name = _name.replace('）',')')
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
    print(f'一共有{len(id_name)}个角色')

    with open('unit_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(id_name, ensure_ascii=False))

    with open('miss.log', 'w', encoding='utf-8') as f:
        f.write(miss)

    os.system('pause')
    pass



