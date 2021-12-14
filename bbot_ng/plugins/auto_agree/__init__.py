#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   bbot_ng\plugins\auto_agree\__init__.py 
@Time    :   2021-12-14 16:53:22 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

from nonebot import on_request, on_notice, on_command
from nonebot.adapters.cqhttp import Event, FriendRequestEvent, GroupRequestEvent
from nonebot.log import logger
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.rule import to_me

friend_req = on_request()


@friend_req.handle()
async def friend_req(bot: Bot, event: FriendRequestEvent, state: T_State):
    logger.debug('friend req called')
    logger.debug(event.json())
    await bot.call_api('set_friend_add_request', flag=event.flag, approve=True)
    # await bot.set_friend_add_request()


group_req = on_request()


@group_req.handle()
async def group_req(bot: Bot, event: GroupRequestEvent, state: T_State):
    logger.debug('group req called')
    logger.debug(event.json())
    logger.debug(event.flag)
    await bot.call_api('set_group_add_request', flag=event.flag, approve=True)
    # await bot.set_group_add_request(approve=True)