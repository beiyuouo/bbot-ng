#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   bbot_ng\plugins\v2rss\v2.py 
@Time    :   2021-11-18 20:14:25 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import random

import json
import httpx

from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event

from .apis import *
from .db import *
from .utils import *

v2 = on_command("vv", rule=to_me(), priority=1, aliases=set(['v2', 'ycj']))

help_msg = """vv [list|help|usage|about]"""

about_msg = """vv is a plugin for v2rss."""


async def help_handle(bot: Bot, event: Event, state: T_State):
    await v2.finish(help_msg)


async def about_handle(bot: Bot, event: Event, state: T_State):
    await v2.finish(about_msg)


async def list_handle(bot: Bot, event: Event, state: T_State):
    try:
        resp = await get_list()
    except Exception as e:
        logger.error(f"{e}")
        await v2.finish(f"No response")

    await v2.finish(format_list(resp))


async def usage_handle(bot: Bot, event: Event, state: T_State):
    usage_factory = {}


async def vv_handle(bot: Bot, event: Event, state: T_State):
    sub_id = state["args"][0] if len(state["args"]) > 0 else None
    logger.debug(f"sub_id: {sub_id}")

    try:
        if sub_id is None:
            resp = await get_list()
            logger.debug(f"resp: {resp}")
            logger.debug(
                f"{random.choice(list(resp['info']['v2ray'].keys()))}")
            sub_id = random.choice(list(resp['info']['v2ray'].keys()))
            logger.debug(f"random sub_id: {sub_id}")
        resp = await get_sub(sub_id)
    except Exception as e:
        logger.error(f"{e}")
        await v2.finish(f"No response")

    await v2.finish(resp)


async def get_list():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(ALKAID_GET_SUBS)
            resp = resp.text
            logger.debug(f"get resp from alkaid: {resp}")
            resp = json.loads(resp)
            return resp
        except json.decoder.JSONDecodeError:
            logger.error(f"resp from alkaid is not json: {resp}")
            await v2.finish(f"JSONDecodeError")


async def get_sub(sub_id: str = '') -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(ALKAID_GET_SUBS_BY_ID + sub_id)
        resp = resp.text
        logger.debug(f"get resp from alkaid: {resp}")
        try:
            resp = json.loads(resp)['info']['subscribe']
            return resp
        except json.decoder.JSONDecodeError:
            logger.error(f"resp from alkaid is not json: {resp}")
            await v2.finish(f"JSONDecodeError")


handle_factory = {
    'list': list_handle,
    'help': help_handle,
    'usage': usage_handle,
    'about': about_handle,
    'vv': vv_handle,
}


@v2.handle()
async def handle(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip().split()
    state["args"] = args
    logger.debug(f"args: {args}")


@v2.got("args")
async def args_handle(bot: Bot, event: Event, state: T_State):
    args = state["args"]
    logger.debug(f'get args: {args}')

    if args:
        cmd = args[0]
        if cmd in handle_factory:
            state["args"] = args[1:]
            await handle_factory[cmd](bot, event, state)
        else:
            try:
                await handle_factory['vv'](bot, event, state)
            except KeyError:
                logger.error(f"{cmd} is not a valid command")
                await v2.finish(f"{cmd} is not a valid command")
    else:
        state["args"] = []
        await vv_handle(bot, event, state)
        # v2.finish(help_msg)
