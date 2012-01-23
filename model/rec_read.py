#coding:utf-8
from _db import redis
from zkit.zitertools import lineiter

REDIS_REC_READ = 'RecRead:%s'

def rec_read(user_id, limit=7):
    limit = limit-1
    key =  REDIS_REC_READ%user_id
    result = redis.zrevrange(key , 0, limit, False)
    redis.zremrangebyrank(key, -limit-1 , -1)
    return result

def rec_read_extend(user_id , id_score_list):
    return redis.zadd(REDIS_REC_READ%user_id, *lineiter(id_score_list))



if __name__ == '__main__':
    pass
    rec_read_extend(1, ((7, 9), (5, 1) , (1, 2), (2, 3)))
    print rec_read(1, 1)
    print rec_read(1, 1)
    print rec_read(1, 1)
    print rec_read(1, 1)
    print rec_read(1, 7)
