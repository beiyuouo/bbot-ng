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
ALKAID_GET_SUBS_STATUS = ALKAID_HOST + config.alkaid_get_subs_status
ALKAID_GET_SUBS_RANDOM = ALKAID_HOST + config.alkaid_get_subs_random
ALKAID_GET_SUBS_BY_ID = ALKAID_HOST + config.alkaid_get_subs_by_id

SUPERUSERS = config.superusers

COOLDOWN = config.cooldown