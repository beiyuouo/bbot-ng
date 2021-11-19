# Author: BeiYu
# Github: https://github.com/beiyuouo
# Date  : 2021/1/22 12:49
# Description:

import nonebot
from nonebot.log import logger

global_config = nonebot.get_driver().config
config = nonebot.Config(**global_config.dict())

logger.info(f"config: {config}")

ALKAID_HOST = config.alkaid_host
ALKAID_GET_SUBS_DEBUG = ALKAID_HOST + config.alkaid_get_subs_debug
ALKAID_GET_SUBS = ALKAID_HOST + config.alkaid_get_subs
ALKAID_GET_SUBS_BY_ID = ALKAID_HOST + config.alkaid_get_subs_by_id

SUPERUSERS = config.superusers

if config.test:
    ALKAID_GET_SUBS_BY_ID = ALKAID_GET_SUBS_DEBUG

COOLDOWN = config.cooldown