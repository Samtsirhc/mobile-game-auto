from modules.tools import *
import os

UNIT_DATA = load_json('pcr_data/unit_name/unit_data.json')

def nick_name2name(name):
    for i in UNIT_DATA:
        if name in UNIT_DATA[i]:
            return UNIT_DATA[i][0]
    else:
        return name


def name2id(name):
    for i in UNIT_DATA:
        if name in UNIT_DATA[i]:
            return str(i)
    else:
        return '000000'

def id2name(id): 
    _id = str(id)
    try:
        return UNIT_DATA[_id][0]
    except:
        return '未知'

def nick_id2id(id):

    _id = str(id)
    _id = _id[:4] + '0' + _id[5:]
    return _id


unit_imgs_path = 'pcr_data/unit_imgs/'
class UnitManager():
    def __init__(self):
        self.imgs_data_path = unit_imgs_path + 'imgs_data.json'
        self.load_imgs(unit_imgs_path)
        self.load_imgs_data()
        pass

    def load_imgs(self, unit_imgs_path):
        _needless = ['imgs_data.json', 'get_unit_img.py']
        self.img_names = os.listdir(unit_imgs_path)
        for i in _needless:
            self.img_names.remove(i)
        self.imgs = {}
        for i in self.img_names:
            self.imgs[i] = load_img(f'{unit_imgs_path}{i}')

    def load_imgs_data(self):
        self.imgs_data = load_json(self.imgs_data_path)['data']
        for i in self.img_names:
            for j in self.imgs_data:
                if j['file_name'] == i:
                    break
            else:
                _id = nick_id2id(i.replace('.webp', ''))
                _tmp = {'file_name': i,
                        'id': _id,
                        'name': id2name(_id),
                        'count': 0}
                self.imgs_data.append(_tmp)
        self.write_imgs_data()

    def write_imgs_data(self):
        self.imgs_data = sorted(
            self.imgs_data, key=lambda i: i['count'], reverse=True)
        write_json(self.imgs_data_path, {'data': self.imgs_data})

    def add_count(self, img_name):
        if '.' not in img_name:
            img_name += '.webp'
        for i in self.imgs_data:
            if i['file_name'] == img_name:
                i['count'] += 1
        self.write_imgs_data()

    def get_img(self, unit, re_type: 0):
        if '1' not in unit and '2' not in unit and type(unit) != int:
            unit = name2id(unit)
        if re_type == 0:
            return self.imgs[unit + '.webp']
        else:
            _ids = []
            _ids.append(str(int(unit) +10))
            _ids.append(str(int(unit) +30))
            _ids.append(str(int(unit) +60))
            _imgs = []
            for i in _ids:
                try:
                    _imgs.append(self.imgs[i + '.webp'])
                except:
                    pass
            return _imgs

    def reg_wife(self, img, resize=80, similarity=0.85):
        _tmp = '未知'
        for i in self.imgs_data:
            _res = 0
            try:
                _bg = self.imgs[i['file_name']]
                _bg = img_resize(_bg, (resize, resize))
                _res = match_image(img, _bg)
            except:
                continue
            # print(f'{_res} *** {i["name"]}')
            if _res > similarity:
                # print(_res)
                self.add_count(i['file_name'])
                # print(i['name'])
                _tmp = i['name']
                print(i['name'])
                break
        return _tmp

if __name__ == "__main__":
    u = UnitManager()
    a = load_img('1.jpg')
    for i in range(110,140):
        b = u.reg_wife(a, i)
        print(f'{b} {i}')
    # 95