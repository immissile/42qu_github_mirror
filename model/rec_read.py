#coding:utf-8
from _db import redis
from zkit.zitertools import lineiter

REDIS_REC_READ = 'RecRead:%s'
REDIS_REC_LOG = 'RecLog:%s'

def rec_read(user_id, limit=7):
    limit = limit-1
    key = REDIS_REC_READ%user_id
    result = redis.zrevrange(key , 0, limit, False)
    if result:
        redis.zremrangebyrank(key, -limit-1 , -1)
        redis.lpush(REDIS_REC_LOG%user_id, *result)
    return result

def rec_read_extend(user_id , id_score_list):
    return redis.zadd(REDIS_REC_READ%user_id, *lineiter(id_score_list))


def rec_read_log(user_id, limit=7, offset=0):
    if offset == 0:
        rec_read(user_id, limit)

    key = REDIS_REC_LOG%user_id
    length = redis.llen(key)

    return  length, redis.lrange(key, offset, offset+limit-1)

from model.po import Po

def po_by_rec_read(user_id, limit=7):
    return Po.mc_get_list(rec_read(user_id, limit))

def po_by_rec_read_equal_limit(user_id, limit=7):
    key = REDIS_REC_READ%user_id
    if redis.zcard(key) < limit:
        return []
    return po_by_rec_read(user_id)


def rec_read_empty(user_id):
    redis.delete(REDIS_REC_READ%user_id)

if __name__ == '__main__':
    user_id = 10000000
    from model.po import Po
    print rec_read_log(user_id)
