#coding:utf-8
from _db import redis
from zkit.zitertools import lineiter
from time import time

REDIS_REC_CID_TUPLE = (
    (1, "网络·科技·创业"),
    (2, "情感·社会·人文"),
    (3, "女性·时尚·星座"),
    (6, "图书·电影·音乐"),
    (7, "职业·成长·学习"),
    (4, "政治·经济·历史"),
    (5, "生活·旅行·居家"),
    (8, "酷知识"),
)

REDIS_REC_CID_DICT = dict(REDIS_REC_CID_TUPLE)

REDIS_REC_CID = "RecCid:%s" 
REDIS_REC_READ = 'RecRead:%s'
REDIS_REC_LOG = 'RecLog:%s'

def rec_read(user_id, limit=7):
    limit = limit-1
    key = REDIS_REC_READ%user_id

    now = int(time() - 1327823396)

    if limit < 0:
        limit = 0

    total = 0
    key_log = REDIS_REC_LOG%user_id

    t = []

    while True:
        result = redis.zrevrange(key , total, total+limit, False)

        offset = 0
        count = 0

        for i in result:
            total += 1

            if redis.zscore(key_log, i):
                continue

            t.append(i)
            t.append(now+offset)
            offset -= 0.1
            count += 1

            if count >= limit:
                break

        if count >= limit or len(result) < limit:
            break

    if t:
        redis.zadd(key_log, *t)

    if total:
        redis.zremrangebyrank(key, -total , -1)

    return result

def rec_read_extend(user_id , id_score_list):
    return redis.zadd(REDIS_REC_READ%user_id, *lineiter(id_score_list))

def rec_read_log(user_id, limit=7, offset=0):
    if offset == 0:
        rec_read(user_id, limit)

    key = REDIS_REC_LOG%user_id

    return  redis.zrevrange(key, offset, offset+limit-1)

def rec_read_log_with_len(user_id, limit=7, offset=0):
    return redis.zcard(key), rec_read_log(user_id, limit, offset)

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

    rec_read_extend(user_id, [(1, 1), (2, 2)])
    print rec_read_log(user_id,1)
    #print rec_read_empty(user_id)

    

