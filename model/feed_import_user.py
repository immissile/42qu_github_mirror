#coding:utf-8
from _db import redis
from model.zsite import Zsite

REDIS_FEED_IMPORT_USER = 'FeedImportUser'
REDIS_FEED_IMPORT_USER_ID_LIST = 'FeedImportUser:%s'


def feed_import_user_new(user_id, feed_import_id):
    if redis.sadd(REDIS_FEED_IMPORT_USER_ID_LIST%user_id, feed_import_id):
        redis.zincrby(REDIS_FEED_IMPORT_USER, user_id, 1)


def feed_import_user_rm(user_id, feed_import_id):
    key = REDIS_FEED_IMPORT_USER_ID_LIST%user_id
    redis.srem(key, feed_import_id)
    length = redis.scard(key)
    if length:
        redis.zadd(REDIS_FEED_IMPORT_USER, user_id, length)
    else:
        redis.zrem(REDIS_FEED_IMPORT_USER, user_id)

def feed_import_user_count():
    return redis.lzcat(REDIS_FEED_IMPORT_USER)

def id_count_by_feed_import_user(limit, offset):
    return redis.zrevrange(REDIS_FEED_IMPORT_USER, offset, limit+offset-1, True, int)

def feed_import_id_by_user_id(user_id):
    return redis.srandmember(REDIS_FEED_IMPORT_USER_ID_LIST%user_id) 


if __name__ == '__main__':
    pass

    user_id = 10000000
    feed_import_id = 1

    feed_import_user_new(user_id, feed_import_id)
    print id_count_by_feed_import_user(11, 0)
    print feed_import_id_by_user_id(user_id)
    feed_import_user_rm(user_id, feed_import_id)
    print feed_import_id_by_user_id(user_id)
    print id_count_by_feed_import_user(11, 0)

