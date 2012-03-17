#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5
from _db import McCache , Model, redis
from decorator import decorator


# zhash
SPAMMER_REDIS_KEY = "zpage:spammer"


#SPAM_USER_ID = set((
#    10009078, #欲望清单 www.desirelist.nst
#    10003899, #欲望清单 www.desirelist.nst
#    10011921,
#    10022520,
#    10133407,
#))

def spammer_new(user_id):
    user_id = int(user_id)
    redis.sadd(SPAMMER_REDIS_KEY, user_id)

def spammer_rm(user_id):
    user_id = int(user_id)
    redis.srem(SPAMMER_REDIS_KEY, user_id)

def is_spammer(user_id):
    return redis.sismember(SPAMMER_REDIS_KEY, user_id)

mc_lastest_hash = McCache('LastestHash:%s')

def is_same_post(user_id, *args):
    m = md5()
    for i in args:
        if type(i) is not str:
            i = str(i)
        m.update(i)
    h = m.digest()
    user_id = str(user_id)
    if h == mc_lastest_hash.get(user_id):
        return True
    mc_lastest_hash.set(user_id, h, 60)
    return False

@decorator
def anti_same_post(func, user_id, *args, **kwds):
    values = kwds.values()
    values.extend(args)
    if is_same_post(user_id, *values):
        return
    return func(user_id, *args, **kwds)

def spammer_reset(user_id):
    from model.po import Po, po_rm, reply_rm_if_can
    from zsite_tag import zsite_tag_rm_by_po
    for i in Po.where(user_id=user_id):
        po_rm(user_id, i.id)
        zsite_tag_rm_by_po(i)

    from model.reply import Reply
    for i in Reply.where(user_id=user_id):
        reply_rm_if_can(user_id, i.id)
    
    
    
    from model.wall import Wall
    from model.zsite import Zsite
    z = Zsite.mc_get(user_id)
    total = z.reply_count
    if total:
        reply_list = z.reply_list_reversed(total,0)
        for reply in reply_list:
            wall = Wall.mc_get(reply.rid)
            if wall:
                wall.reply_rm(reply)
    

    spammer_new(user_id)
        




if __name__ == '__main__':

    spammer_reset(10207348)
