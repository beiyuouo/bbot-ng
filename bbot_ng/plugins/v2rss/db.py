#!/usr/bin/env python
# -*- encoding: utf-8 -*-
""" 
@File    :   bbot_ng\plugins\v2rss\db.py 
@Time    :   2021-11-18 20:43:27 
@Author  :   Bingjie Yan 
@Email   :   bj.yan.pa@qq.com 
@License :   Apache License 2.0 
"""

import os
import uuid
import sqlite3

from nonebot.log import logger

os.makedirs('dbs', exist_ok=True)
db = sqlite3.connect(os.path.join('dbs', 'v2rss.db'))
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS v2rss (
        uuid TEXT PRIMARY KEY,
        user_id TEXT,
        timestamp INTEGER,
        sub TEXT)
''')


async def get_usage(time_after: int):
    cursor.execute('SELECT COUNT(*) FROM v2rss WHERE timestamp > ?',
                   (time_after, ))
    return cursor.fetchone()


async def get_usage_by_user(user_id: str):
    cursor.execute(
        '''
        SELECT COUNT(*) FROM v2rss WHERE user_id = ? GROUP BY sub
    ''', (user_id, ))

    return cursor.fetchall()


async def insert_usage(user_id: str, timestamp: int, sub: str):
    cursor.execute(
        '''
        INSERT INTO v2rss (uuid, user_id, timestamp, sub)
        VALUES (?, ?, ?, ?)
    ''', (str(uuid.uuid1()), user_id, timestamp, sub))
    logger.debug(
        f"insert_usage: {str(uuid.uuid1())}, {user_id}, {timestamp}, {sub}")
    db.commit()


async def get_last_time(user_id):
    cursor.execute(
        '''
        SELECT timestamp FROM v2rss WHERE user_id = ?
    ''', (user_id, ))
    return cursor.fetchone()


if __name__ == '__main__':
    pass