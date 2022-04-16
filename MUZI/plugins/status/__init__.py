import re
from typing import Tuple
from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.params import RegexGroup

from MUZI.config import BotInfo
from .source import get_status

cmd1 = on_command("状态", permission=SUPERUSER)
@cmd1.handle()
async def _(event: MessageEvent):
    await cmd1.finish(get_status())

cmd2 = on_regex(r"^插件\s?(开启|关闭|已开启)?\s?(.*)?", flags=re.I)
@cmd2.handle()
async def _(event: GroupMessageEvent, args: Tuple = RegexGroup()):
    if not args[0] and args[1].isdigit():
        if int(args[1])<=len(BotInfo.plugins):
            await cmd2.send(BotInfo.plugins[int(args[1])-1]+'\n'+BotInfo.plugin_describe[BotInfo.plugins[int(args[1])-1]])
        else:
            await cmd2.send(f'{BotInfo.name}没有这个能力呢~')
    elif args[0] == '开启' and args[1].isdigit():
        if int(args[1])<=len(BotInfo.plugins):
            p = BotInfo.plugins[int(args[1])-1]
            id = event.group_id
            if p in BotInfo.optional_plugin:
                if id not in BotInfo.plugins_setting[p]:
                    BotInfo.plugins_setting[p].append(id)
                    BotInfo.update_plugin_setting(**BotInfo.plugins_setting)
                else:
                    await cmd2.send(f'{p}已经开启了呀~')
            else:
                await cmd2.send(f'{p}是默认插件{BotInfo.name}没权限更改QAQ')
    elif args[0] == '关闭' and args[1].isdigit():
        if int(args[1])<=len(BotInfo.plugins):
            p = BotInfo.plugins[int(args[1])-1]
            id = event.group_id
            if p in BotInfo.optional_plugin:
                if id in BotInfo.plugins_setting[p]:
                    BotInfo.plugins_setting[p].remove(id)
                    BotInfo.update_plugin_setting(**BotInfo.plugins_setting)
                else:
                    await cmd2.send(f'{p}已经关闭了呀~')
            else:
                await cmd2.send(f'{p}是默认插件{BotInfo.name}没权限更改QAQ')
    elif args[0] == '已开启':
        await cmd2.send(f'{BotInfo.name}可用在这里使用这些能力:\n'+
            '\n'.join([f'{BotInfo.plugins.index(i)+1}. {i}' for i in BotInfo.default_plugin])+'\n'+
            '\n'.join([f'{BotInfo.plugins.index(i)+1}. {i}' for i in BotInfo.plugins_setting if event.group_id in BotInfo.plugins_setting[i]])
            )
    else:
        await cmd2.send('插件(插件编号)  查看插件用法\n插件(开启/关闭)(插件编号/all)  在群中启用或关闭插件\n插件已开启  查看群内已开启插件')
        await cmd2.send(
            f'{BotInfo.name}的所有能力:\n总是开启:\n'+
            '\n'.join([f'{BotInfo.plugins.index(i)+1}. {i}' for i in BotInfo.default_plugin])+
            '\n可选插件:\n'+
            '\n'.join([f'{BotInfo.plugins.index(i)+1}. {i}' for i in BotInfo.optional_plugin])
            )