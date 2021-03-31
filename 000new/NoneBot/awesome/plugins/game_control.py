from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment
import os
import random
import nonebot
import requests

SCRIPT_PATH = r'../../'

# on_command 装饰器将函数声明为一个命令处理器
@on_command('方舟', aliases=('方舟'))
async def 方舟(session: CommandSession):
    os.system(f"start {SCRIPT_PATH}方舟日常.py")  
    reply = await game_script()
    await session.send(reply)

@on_command('pcr', aliases=('pcr'))
async def pcr(session: CommandSession):
    os.system(f"start {SCRIPT_PATH}pcr日常.py")  
    reply = await game_script()
    await session.send(reply)

async def game_script():
    return f'收到'

