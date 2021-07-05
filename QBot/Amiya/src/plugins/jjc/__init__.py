from nonebot import on_message, on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests

ask = on_message(priority=99)
url = "http://127.0.0.1:8888/"

@ask.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    state = {'raw_message':str(event.get_message()), 'group_id':0,'user_id':0}
    state['user_id'] = int(event.get_user_id())
    session = str(event.get_session_id())
    message = state['raw_message']
    if message.startswith('怎么拆') or message.startswith('jjc查询'):
        _res = await send_info(message)
        await ask.finish(_res)



async def send_info(name: str):
    try:
        _res = requests.post(url, data = str(name).encode())
        return _res.content.decode()
    except Exception as e:
        return "出了点问题，问题是" + str(e)

