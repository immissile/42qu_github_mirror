#coding:utf-8
from _db import  McModel, Model, McLimitA, McNum, McCacheA, redis


#标签 - 用户数
#标签%id - 用户 id list 
#用户%id - 标签 id list
 
#标签 - 文章数
#文章%id - 标签 id list
#标签%id - 文章 id list

REDIS_PO_TAG_USER = "PoTagUser:%s"
REDIS_UESR_PO_TAG = "UserPoTag:%s" 

class PoUserTag(object):
    def __init__(self, key):
        pass

 

#def po_tag_user_new(user_id, po_tag_id):
#    p = redis.pipeline()
#    key = REDIS_PO_TAG_USER%po_tag_id
#    redis.hset(key, p)
#
#    p.execute() 


if __name__ == '__main__':
    pass

