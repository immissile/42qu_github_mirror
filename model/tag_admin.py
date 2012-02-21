#coding:utf-8
from _db import redis

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

def tag_list_count_by_tag_admin(limit, offset):
    id_count = redis.zrevrange(REDIS_TAG_ADMIN, offset, offset+limit-1, True, int)
    return id_count

#def po_list_by_tag_admin(tag_id, limit, offset):
#    pass

if __name__ == '__main__':
    pass

    print tag_list_count_by_tag_admin(100, 0)

