from nonebot import on_message, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import random
import jieba
import jieba.posseg as pseg
jieba.setLogLevel(20)

ask = on_message(priority=98)
h_level = 0.5

@ask.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    state = {'raw_message':str(event.get_message()), 'group_id':0,'user_id':0}
    state['user_id'] = int(event.get_user_id())
    session = str(event.get_session_id())
    message = state['raw_message']
    if message.startswith('翻译') or message.startswith('说'):
        _res = await send_info(message)
        await ask.finish(_res)



async def send_info(name: str):
    try:
        msg = ""
        if name.startswith('翻译'):
            msg = name[2:]
        if name.startswith('说'):
            msg = name[1:] 
        msg = chs2yin(name, h_level)
        return msg
    except Exception as e:
        return "出了点问题，问题是" + str(e)

def _词转换(x, y, 淫乱度):
    if random.random() > 淫乱度:
        return x
    if x in {'，', '。'}:
        return '……'
    if x in {'!', '！'}:
        return '❤'
    if len(x) > 1 and random.random() < 0.5:
        return f'{x[0]}……{x}'
    else:
        if y == 'n' and random.random() < 0.5:
            x = '〇' * len(x)
        return f'……{x}'


def chs2yin(s, 淫乱度=0.5):
    return ''.join([_词转换(x, y, 淫乱度) for x, y in pseg.cut(s)])