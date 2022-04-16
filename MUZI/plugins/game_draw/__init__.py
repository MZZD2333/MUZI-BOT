import re
from typing import Tuple

from bs4 import BeautifulSoup
from httpx import AsyncClient
from MUZI.config import BotInfo
from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import RegexGroup
from nonebot.permission import SUPERUSER
from nonebot.adapters.onebot.v11.helpers import Cooldown
from .Arknights import Arknights_draw
from .updata import *

matcher = on_command('test',permission=SUPERUSER)
@matcher.handle()
async def _(event: MessageEvent):
    await check_updata_all()
    await matcher.finish(str(Ark.cache))

Ark_matcher = on_regex(r'^(明日)?方舟(10|[1-9]|单|十)[抽|发|连]')
@Ark_matcher.handle([Cooldown(5)])
async def _(event: MessageEvent, arg:Tuple = RegexGroup()):
    单, 十 = 1, 10
    times = eval(f'{arg[1]}')
    await Ark_matcher.finish(Message(await Arknights_draw(times, event.user_id)+f'\n累计{Ark.cache[event.user_id]}抽未出六星'), at_sender = True)


Ark_cache_matcher = on_regex(r'^清理方舟缓存')
@Ark_cache_matcher.handle()
async def _(event: MessageEvent):
    Ark.cache = {}
    await Ark_cache_matcher.finish(f'{BotInfo.name}清理好了')
