import asyncio
import re
from typing import Tuple

from nonebot.adapters.onebot.v11 import Message, MessageEvent, PrivateMessageEvent, PRIVATE_FRIEND, GROUP
from nonebot.params import RegexGroup
from nonebot.plugin import on_regex

from .source import get_setu

matcher = on_regex(r"^st\s?([1-9])?\s?(r)?\s?(.*)?", flags=re.I, permission=PRIVATE_FRIEND | GROUP, priority=1)
@matcher.handle()
async def _(event: MessageEvent, args: Tuple = RegexGroup()):
    n = args[0]
    r18 = args[1]
    key = args[2]
    n = int(n) if n else 1
    r18 = True if (isinstance(event, PrivateMessageEvent) and r18) else False
    task = []
    async def _main():
        setu = await get_setu(key, r18)
        if setu:
            await matcher.send(Message(setu))
    for i in range(n):
        task.append(_main())
    await asyncio.wait(task)
