from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
import requests

script = on_command("运行脚本", rule=to_me(), priority=1)
url = "http://127.0.0.1:8888/"

@script.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()  # 首次发送命令时跟随的参数，
    if args:
        state["name"] = args  # 如果用户发送了参数则直接赋值


@script.got("name", prompt="运行什么脚本？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    name = state["name"]
    _res = await send_info(name)
    await script.finish(_res)


async def send_info(name: str):
    _res = requests.post(url, data = str(name))
    return _res.content.decode()