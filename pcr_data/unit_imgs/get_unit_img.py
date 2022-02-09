# pip install beautifulsoup4
from bs4 import BeautifulSoup as bf
import requests
import os
import string

def save_img(img, name):
    with open(name, 'wb') as f:
        f.write(img)
    print(name)

def get_img(name):
    url = 'https://redive.estertion.win/icon/unit/' + name + '@w400'
    re = requests.get(url)
    re = re.content
    save_img(re, name)

def get_img_names():
    url = 'https://redive.estertion.win/icon/unit'
    re = requests.get(url)
    re = re.content
    soup = bf(re, 'lxml')
    # print(soup.prettify())
    names = soup.select("a[href]")
    name_list = []
    for i in names:
        # print(i['href'])
        name_list.append(i['href'])
    return name_list


def webp2jpg(img):
    pass
if __name__ == "__main__":
    name_list = get_img_names()
    for i in name_list:
        _tmp = i
        if '_' in _tmp:
            continue
        if int(_tmp.replace('.webp', '')) > 200000:
            break
        try:
            _size = os.path.getsize(i)
            if _size > 2000 and _size < 10000:
                print(f'{i} 已存在')
                continue
            else:
                raise FileNotFoundError
        except FileNotFoundError:
            get_img(i)
    print("==========现在开始更新imgs_data.json==========")
    os.system('pause')





