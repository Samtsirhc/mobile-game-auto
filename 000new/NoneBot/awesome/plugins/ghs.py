from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment
import os
import random
import nonebot
import requests

# on_command 装饰器将函数声明为一个命令处理器
@on_command('ghs', aliases=('色图', 'ghs', '冲', 'gkd'))
async def ghs(session: CommandSession):
    h_pic = await get_h_pic()
    await session.send(h_pic)


async def get_h_pic():
    # 返回色图
    # url = 'http://api.mtyqx.cn/api/random.php' 
    # r = requests.get(url)
    pic_name = "1"
    pic_dir_path = r"C:\Users\lcyba\Desktop\\"
    # with open(f"{pic_dir_path}{pic_name}.jpg", "wb") as code:
    #     code.write(r.content)
    a = r"1.jpg"
    return f'[CQ:image,file={a}]'
    # return "1"