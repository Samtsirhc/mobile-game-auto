from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment
import os
import random
import nonebot
import requests

@on_command('dice', aliases=('丢骰子'), only_to_me=False)
async def dice(session: CommandSession):
    user_id = session.event["user_id"]
    _number = await dice_number()
    reply = f'[CQ:at,qq={user_id}]你丢的点数是【{_number}】'
    await session.send(reply)

async def dice_number():
    return random.randint(1,6)