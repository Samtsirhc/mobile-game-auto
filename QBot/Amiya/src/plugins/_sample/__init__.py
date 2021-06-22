import nonebot
from .config import Config

global_config = nonebot.get_driver().config
plugin_config = Config(**global_config.dict())