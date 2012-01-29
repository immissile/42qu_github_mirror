#coding:utf-8
from _db import redis
from zkit.zitertools import lineiter
from time import time


REDIS_REC_READ = 'RecRead:%s'
REDIS_REC_LOG = 'RecLog:%s'

def rec_read(user_id, limit=7):
    limit = limit-1
    key = REDIS_REC_READ%user_id

    now = int(time() - 1327823396)

    if limit < 0:
        limit = 0

    count = limit
    key_log = REDIS_REC_LOG%user_id

    while count:
        result = redis.zrevrange(key , 0, limit, False)
        if result:
            redis.zremrangebyrank(key, -len(result) , -1)
            
            t = []

            offset = 0
            for i in result:
                if redis.zscore(key_log, i):
                    continue
                t.append(i)
                t.append(now+offset)
                offset += 0.1
                count -= 1
                
            redis.zadd(key_log, *t)
        else:
            break

    return result

def rec_read_extend(user_id , id_score_list):
    return redis.zadd(REDIS_REC_READ%user_id, *lineiter(id_score_list))

def rec_read_log(user_id, limit=7, offset=0):
    if offset == 0:
        rec_read(user_id, limit)

    key = REDIS_REC_LOG%user_id
    length = redis.zcard(key)
     
    return  length, redis.zrevrange(key, offset, offset+limit-1)

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
    redis.delete(REDIS_REC_LOG%user_id)

if __name__ == '__main__':
    user_id = 10000000
    from model.po import Po

    rec_read_extend(user_id, [(1,4),(2,1)])
    print rec_read_log(user_id)
    print rec_read_empty(user_id)
