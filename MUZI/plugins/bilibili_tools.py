import re
from typing import Tuple

import requests
from nonebot import on_regex
from nonebot.adapters.onebot.v11 import Message, MessageEvent
from nonebot.params import RegexGroup

from MUZI.config import BotInfo

matcher = on_regex(r'^封面\s?(av\d*|BV.*)', flags=re.I, priority=1)

@matcher.handle()
async def _(event: MessageEvent, match: Tuple = RegexGroup()):
    bvid = match[0]
    bvid = f'aid={bvid[2:]}' if 'av' == bvid[:2].lower() else f'bvid={bvid}'
    url = 'https://api.bilibili.com/x/web-interface/view?' + bvid
    data = requests.get(url).json()
    msg = f"[CQ:image,file={data['data']['pic']}]" if data['code'] == 0 else f'{match[0]}好像找不到了呢'
    await matcher.send(Message(msg))
