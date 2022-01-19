#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   bbot_ng\plugins\v2rss\v2.py 
@Time    :   2021-11-18 20:14:25 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

from re import sub
import time
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

help_msg = """vv [list|help|usage|about]\n · list: list all v2ray subscribe\n · help: show this message\n · usage: show usage of vv（admin)\n · about: show about of vv"""

about_msg = """vv is a plugin for v2rss maintained by @BeiYu. v2rss is a v2ray subscribe collector maintain by @QIN2DIM."""


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
    usage_factory = {
        'today': get_usage(int(time.time()) - 24 * 60 * 60),
        'week': get_usage(int(time.time()) - 7 * 24 * 60 * 60),
        'month': get_usage(int(time.time()) - 30 * 24 * 60 * 60),
        'year': get_usage(int(time.time()) - 365 * 24 * 60 * 60),
        'all': get_usage(0),
    }
    args = state["args"][0] if len(state["args"]) > 0 else None
    logger.debug(f"args: {args}")

    if args in usage_factory.keys():
        usage_func = usage_factory[args]
        usage = await usage_func
        usage = usage[0] if usage else None
        if usage:
            await v2.finish(f'{args} usage: {usage}')
        else:
            await v2.finish(f'No {args} usage')
    else:
        await v2.finish(f"usage: {usage_factory.keys()}")


async def vv_handle(bot: Bot, event: Event, state: T_State):
    sub_id = state["args"][0] if len(state["args"]) > 0 else None
    logger.debug(f"sub_id: {sub_id}")
    logger.debug(f"user_id:{event.user_id}")

    last_ = await get_last_time(event.user_id)
    last_ = int(last_[0]) if last_ else None
    logger.debug(f"last_: {last_}")
    if last_ is not None and time.time() - last_ < COOLDOWN:
        await v2.finish(f"You are too fast")

    try:
        if sub_id is None:
            resp = await get_random_sub()
        else:
            resp = await get_sub(sub_id)
    except Exception as e:
        logger.error(f"{e}")
        await v2.finish(f"{e.args[0]}")

    await insert_usage(event.user_id, int(time.time()), sub_id)
    await v2.finish(resp)


async def get_list():
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(ALKAID_GET_SUBS_STATUS)
            resp = resp.text
            logger.debug(f"get resp from alkaid: {resp}")
            resp = json.loads(resp)
            return resp
        except json.decoder.JSONDecodeError:
            logger.error(f"resp from alkaid is not json: {resp}")
            raise Exception(f"JSONDecodeError")


async def get_sub(sub_id: str = '') -> str:
    async with httpx.AsyncClient() as client:
        if temp_dict is None or len(temp_dict) == 0 or lower2original.keys() is None or len(
                lower2original) == 0:
            await v2.send(f"Please use vv list first")
            raise Exception(f"EmptyError")

        if sub_id.isnumeric():
            if sub_id in temp_dict.keys():
                sub_id = temp_dict[sub_id]
            else:
                raise Exception("UnknownError")

        sub_id = sub_id.replace(' ', '')
        sub_id = sub_id.lower()
        sub_id = lower2original[sub_id] if sub_id in lower2original.keys() else sub_id

        resp = await client.post(ALKAID_GET_SUBS_BY_ID, json={'alias': f'Action{sub_id}Cloud'})
        resp = resp.text
        logger.debug(f"get resp from alkaid: {resp}")
        try:
            resp = json.loads(resp)
            if resp['msg'] != 'success':
                raise Exception("RequestError")
            else:
                return resp['subscribe']
        except json.decoder.JSONDecodeError:
            logger.error(f"resp from alkaid is not json: {resp}")
            raise Exception(f"JSONDecodeError")


async def get_random_sub() -> str:
    async with httpx.AsyncClient() as client:
        resp = await client.get(ALKAID_GET_SUBS_RANDOM)
        resp = resp.text
        logger.debug(f"get resp from alkaid: {resp}")
        try:
            resp = json.loads(resp)['subscribe']
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
        if cmd in handle_factory.keys():
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
