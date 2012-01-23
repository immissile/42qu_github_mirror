#coding:utf-8
from _db import redis
from zkit.zitertools import lineiter

REDIS_REC_READ = 'RecRead:%s'

def rec_read(user_id, limit=7):
    limit = limit-1
    key = REDIS_REC_READ%user_id
    result = redis.zrevrange(key , 0, limit, False)
    redis.zremrangebyrank(key, -limit-1 , -1)
    return result

def rec_read_extend(user_id , id_score_list):
    return redis.zadd(REDIS_REC_READ%user_id, *lineiter(id_score_list))


from model.po import Po

def po_by_rec_read(user_id, limit=7):
    return Po.mc_get_list(rec_read(user_id, limit))

def po_by_rec_read_equal_limit(user_id, limit=7):
    id_list = rec_read(user_id, limit)
    if len(id_list) >= limit:
        return Po.mc_get_list(id_list)
    return []

if __name__ == '__main__':
    pass
    print po_by_rec_read(1, 3)


