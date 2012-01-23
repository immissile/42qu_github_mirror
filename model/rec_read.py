#coding:utf-8
from _db import redis


REDIS_REC_READ = "RecRead:%s"

def rec_read(user_id, limit):
    result = redis.zrange(REDIS_REC_READ%user_id, 0, 7, False) 
    return result 

def rec_read_extend(user_id , id_score_list):
    return redis.zadd(REDIS_REC_READ%user_id, *id_score_list)



if __name__ == "__main__":
    pass
    rec_read_extend(1, (1,2, 2, 3))
