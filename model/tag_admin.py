#coding:utf-8
from _db import redis
from model.zsite import Zsite
from operator import itemgetter

REDIS_TAG_ADMIN = 'TagAdmin'
REDIS_TAG_ADMIN_TAG_ID = 'TagAdmin:%s'


def tag_admin_new(id, tag_id_list, rank):
    id = str(id)
    for tag_id in tag_id_list:
        key = REDIS_TAG_ADMIN_TAG_ID%tag_id
        if not redis.zrank(key, id):
            p = redis.pipeline()
            p.zadd(key, id, rank)
            p.zincrby(REDIS_TAG_ADMIN, tag_id, 1)
            p.execute()


def tag_admin_rm(id, tag_id_list):
    id = str(id)
    for tag_id in tag_id_list:
        key = REDIS_TAG_ADMIN_TAG_ID%tag_id
        if redis.zrank(key, id):
            p = redis.pipeline()
            p.zrem(key, id)
            p.zincrby(REDIS_TAG_ADMIN, tag_id, -1)
            p.execute()

def tag_id_name_count_list_by_tag_admin(limit, offset):
    id_count = redis.zrevrange(REDIS_TAG_ADMIN, offset, offset+limit-1, True, int)
    zsite_list = Zsite.mc_get_list(map(itemgetter(0), id_count))
    r = []
    for i,count in zip(zsite_list, map(itemgetter(1),id_count)):
        r.append((i.id, i.name, count)) 

    return r, redis.zcard(REDIS_TAG_ADMIN)


def id_by_tag_admin(tag_id,  offset):
    return redis.zrevrange(
        REDIS_TAG_ADMIN_TAG_ID%tag_id,
        offset,offset
    )

if __name__ == '__main__':
    pass
    
    limit = 50
    offset = 0
    print id_by_tag_admin(10230364L, 0)
    print tag_id_name_count_list_by_tag_admin(limit, offset)
