#coding:utf-8
from _db import redis

REDIS_TAG_ADMIN = "TagAdmin"
REDIS_TAG_ADMIN_PO_ID = "TagAdmin:%s"

def tag_admin_new(po_id, tag_id_list, rank):
    po_id = str(po_id)
    for tag_id in tag_id_list:
        key = REDIS_TAG_ADMIN_PO_ID%tag_id
        if not redis.zcard(key, po_id):
            p = redis.pipeline()
            p.zadd(key, po_id, rank)
            p.zincrby(REDIS_TAG_ADMIN, 1, po_id) 
            p.execute()


def tag_admin_rm(po_id, tag_id_list):
    po_id = str(po_id)
    for tag_id in tag_id_list:
        key = REDIS_TAG_ADMIN_PO_ID%tag_id
        if redis.zcard(key, po_id):
            p = redis.pipeline()
            p.zrem(key, po_id)
            p.zincrby(REDIS_TAG_ADMIN, -1, po_id) 
            p.execute()

def tag_list_count_by_tag_admin(limit, offset):
    id_count = redis.zrevrange(REDIS_TAG_ADMIN, offset, offset+limit-1, True, int)

def po_list_by_tag_admin(tag_id, limit, offset):
    pass

if __name__ == "__main__":
    pass



