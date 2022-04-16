import asyncio
from datetime import datetime
from random import randint, choice

from MUZI.config import BotInfo
from nonebot import on_command, on_notice, on_request
from nonebot.adapters.onebot.v11 import *
from nonebot.adapters.onebot.v11.helpers import Cooldown
from nonebot.matcher import Matcher
from nonebot.params import ArgPlainText, CommandArg
from nonebot.rule import to_me

reporter = on_command("报告", aliases={"反馈"})
@reporter.handle([Cooldown(120, prompt='反馈有120s的cd哦  请稍等\n直接私聊主人也是可以的\n这是主人的qq号: 3314571344')])
async def _ready_repo(matcher: Matcher, args: Message = CommandArg()):
    msg = args.extract_plain_text()
    if msg:
        matcher.set_arg("repo", args)

@reporter.got("repo", f"要跟{BotInfo.name}的主人反馈什么呢?~")
async def _deal_repo(bot: Bot,event: MessageEvent,msg: str = ArgPlainText("repo")):
    user_id = event.get_user_id()
    repo= f'发送人: {user_id}\n内容:\n{msg}'
    for su in BotInfo.superuser:
        await bot.send_private_msg(user_id=su, message="主人 您有收到一条反馈信息呢")
        await bot.send_private_msg(user_id=su, message=repo)
    await reporter.finish(f"{BotInfo.name}已经转达给主人了")


friend_add_event = on_request()
@friend_add_event.handle()
async def _friend_add(bot: Bot, event: FriendRequestEvent):
    apply_comment = event.comment
    user_id = event.get_user_id()
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    repo = f"{now_time}\n主人 我要交到新朋友了\n请求人: {user_id}\n申请信息:\n{apply_comment}"
    for su in BotInfo.superuser:
        await bot.send_private_msg(user_id=su, message=repo)


group_admin_event = on_notice(rule=to_me())
@group_admin_event.handle()
async def _group_admin_event(bot: Bot, event: GroupAdminNoticeEvent):
    repo = f"好欸！主人！我在群 {event.group_id} 成为了管理！！"
    for su in BotInfo.superuser:
        await bot.send_private_msg(user_id=su, message=repo)
    for bg in BotInfo.bindgroup:
        await bot.send_group_msg(group_id=bg, message=repo)


group_ban_event = on_notice(rule=to_me())
@group_ban_event.handle()
async def _group_ban_event(bot: Bot, event: GroupBanNoticeEvent):
    if event.duration:
        now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        repo = f"{now_time}\n主人! 我在群 {event.group_id}\n被 {event.operator_id}\n禁言了{event.duration} 秒"
        for su in BotInfo.superuser:
            await bot.send_private_msg(user_id=su, message=repo)
    else:
        repo = f"好欸！主人\n我在群 {event.group_id}\n被{event.operator_id}解除禁言了！"
        for su in BotInfo.superuser:
            await bot.send_private_msg(user_id=su, message=repo)


group_invite_event = on_request()
@group_invite_event.handle()
async def _group_invite(bot: Bot, event: GroupRequestEvent):
    apply_comment = event.group_id
    user_id = event.get_user_id()
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    repo = f"{now_time}\n 又有新地方可以去玩了\n请求人: {user_id}\n邀请群: {apply_comment}\n"
    for su in BotInfo.superuser:
        await bot.send_private_msg(user_id=su, message=repo)


group_member_event = on_notice()
@group_member_event.handle()
async def _group_member_join(bot: Bot, event: GroupIncreaseNoticeEvent):
    await asyncio.sleep(randint(1, 6))
    msg = f"好欸！事新人！\n我是{choice(list(BotInfo.nickname))}哒!w!\n主人说我是个不太聪明的机器人 嘿嘿  "
    await group_member_event.finish(msg)