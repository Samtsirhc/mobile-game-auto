import os
from PIL import Image

high_size = 30  # 高
width_size = 300  # 宽
out_put = '000.jpg'


def get_img_names():
    img_name = os.listdir()
    for i in img_name:
        if '.py' in i:
            img_name.remove(i)
        if out_put in i:
            img_name.remove(i)
    return img_name


def get_imgs(names):
    _imgs = []
    for i in names:
        _imgs.append(Image.open(i))
    return _imgs


img_names = get_img_names()
imgs = get_imgs(img_names)
left = 0
right = high_size

w = 300
h = 2000

x = w/2
y = 0
_y = int(y)
for image in imgs:
    width = image.size[0]
    height = image.size[1]
    _y += height + 10

target = Image.new('RGB', (w, _y))  # 最终拼接的图像的大小
_y = int(y)
for image in imgs:
    width = image.size[0]
    height = image.size[1]
    _x = int(150 - width/ 2)
    target.paste(image, (_x, _y))
    _y += height + 10
target.save(out_put, quality=100)
