#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from config import MEMCACHED_ADDR, DISABLE_LOCAL_CACHED
from config import REDIS_CONFIG
from zsql.db.mc_connection import init_mc


init_mc(memcached_addr=MEMCACHED_ADDR, disable_local_cached=DISABLE_LOCAL_CACHED)


from config import DB_CONFIG
from zsql.db import connection
connection.THREAD_SAFE = False

from zsql.db import sqlstore
SQLSTORE = sqlstore.SqlStore(db_config=DB_CONFIG, charset='utf8')

def db_by_table(table):
    return SQLSTORE.get_db_by_table(table)

def cursor_by_table(table):
    return db_by_table(table).cursor()

def exe_sql(sql, para=(), table='*'):
    cursor = cursor_by_table(table)
    cursor.execute(sql, para)
    cursor.connection.commit()
    return cursor

connection.get_db_by_table = db_by_table

from zsql.shortcut import Query, mc, McCacheA, McCacheM, McCache,  Model, McModel
from zsql.db.mc import McLimit, McLimitA, McLimitM, McNum

import redis
redis = redis.Redis(**REDIS_CONFIG)

#print redis
