#!/usr/bin/env python
# -*- coding: utf-8 -*-
from hashlib import md5
from _db import McCache , Model, redis
from decorator import decorator
from zsite import Zsite


# zhash
SPAMMER_REDIS_KEY = 'ZpageSpammer'
# is a set, contains reporters
# %s is the id of the reported spammer
SPAMMER_REPORT_KEY = 'ReportedSpammer:%s'
MUTE_FOR_DURATION = 'MutedFor:%s'


#SPAM_USER_ID = set((
#    10009078, #欲望清单 www.desirelist.nst
#    10003899, #欲望清单 www.desirelist.nst
#    10011921,
#    10022520,
#    10133407,
#))

def report_spammer(reporter_id, reportee_id):
    redis.sadd(SPAMMER_REPORT_KEY%reportee_id, reporter_id)

def remove_report(spammer_id):
    redis.delete(SPAMMER_REPORT_KEY%spammer_id)

def confirm_spammer(spammer_id):
    spammer_new(spammer_id)
    remove_report(spammer_id)

def get_all_reports():
    keys = redis.keys(SPAMMER_REPORT_KEY%'*')
    return ((key.replace(SPAMMER_REPORT_KEY%'', ''), redis.smembers(key)) for key in keys)

def mute_for_duration(user_id, duration):
    key = MUTE_FOR_DURATION%user_id
    redis.set(key, duration)
    redis.expire(key, duration)

def get_all_spamer_idlist():
    id_list = redis.smembers(SPAMMER_REDIS_KEY)
    return id_list

def spammer_new(user_id):
    user_id = int(user_id)
    redis.sadd(SPAMMER_REDIS_KEY, user_id)

def spammer_rm(user_id):
    user_id = int(user_id)
    redis.srem(SPAMMER_REDIS_KEY, user_id)

def is_spammer(user_id):
    return redis.sismember(SPAMMER_REDIS_KEY, user_id) or redis.get(MUTE_FOR_DURATION%user_id)

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
        reply_list = z.reply_list_reversed(total, 0)
        for reply in reply_list:
            wall = Wall.mc_get(reply.rid)
            if wall:
                wall.reply_rm(reply)


    spammer_new(user_id)

if __name__ == '__main__':
    for id in get_all_spamer_idlist():
        spammer =  Zsite.get(id)
        print spammer.id, spammer.name, spammer.link
#spammer_reset(10207348)
