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
import sqlite3

os.makedirs('dbs', exist_ok=True)
db = sqlite3.connect(os.path.join('dbs', 'v2rss.db'))
cursor = db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS v2rss (
        uuid TEXT PRIMARY KEY,
        user_id TEXT,
        datetime DATETIME,
        sub TEXT)
''')


def get_usage():
    pass


def get_usage_by_user(user_id):
    cursor.execute(
        '''
        SELECT uuid, datetime, sub FROM v2rss WHERE user_id = ?
    ''', (user_id, ))

    cursor.execute(
        '''
        SELECT COUNT(*) FROM v2rss WHERE user_id = ?
    ''', (user_id, ))
    return cursor.fetchone()


def insert_usage(uuid, user_id, datetime, sub):
    cursor.execute(
        '''
        INSERT INTO v2rss (uuid, user_id, datetime, sub)
        VALUES (?, ?, ?, ?)
    ''', (uuid, user_id, datetime, sub))
    db.commit()


def check_time(user_id):
    cursor.execute(
        '''
        SELECT datetime FROM v2rss WHERE user_id = ?
    ''', (user_id, ))
    return cursor.fetchone()


if __name__ == '__main__':
    pass