#coding:utf-8
from _db import  McModel, Model, McLimitA, McNum, McCacheA, redis

REDIS_PO_TAG_USER = "PoTagUser:%s"
REDIS_UESR_PO_TAG = "UserPoTag:%s" 

#def po_tag_user_new(user_id, po_tag_id):
#    p = redis.pipeline()
#    key = REDIS_PO_TAG_USER%po_tag_id
#    redis.hset(key, p)
#
#    p.execute() 


if __name__ == '__main__':
    pass

