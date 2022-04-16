import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from .config import START_CONFIG


def asgi():
    return nonebot.get_asgi()

def driver():
    return nonebot.get_driver()

def init():
    nonebot.init(**START_CONFIG)
    driver().register_adapter(Adapter)
    nonebot.load_plugins("MUZI/plugins")

def run():
    nonebot.run()