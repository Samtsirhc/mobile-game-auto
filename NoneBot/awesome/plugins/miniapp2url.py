from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment
import os
import random
import nonebot
import requests

# # on_command 装饰器将函数声明为一个命令处理器
# @on_command('ghs', aliases=('色图', 'ghs', '冲', 'gkd'))
# async def miniapp2url(session: CommandSession):
#     _url = await get_url()
#     await session.send(_url)


# async def get_url():
#     return 1