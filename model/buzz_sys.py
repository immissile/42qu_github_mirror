#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitM, McNum
from gid import gid

class BuzzSys(McModel):
    pass

mc_buzz_sys_init_id_list = McCacheA('BuzzSysInitIdList.%s')

@mc_buzz_sys_init_id_list('')
def buzz_sys_init_id_list():
    return BuzzSys.where('seq>0').order_by('seq').col_list()

def buzz_sys_init_list():
    id_list = buzz_sys_init_id_list()
    return BuzzSys.mc_get_list(id_list)

def buzz_sys_list(limit, offset):
    return BuzzSys.where().order_by('id desc')[offset: limit+offset]

def buzz_sys_count():
    return BuzzSys.where().count()

def buzz_sys_new_user(user_id):
    from buzz import buzz_sys_new
    for i in buzz_sys_init_id_list():
        buzz_sys_new(user_id, i)

def buzz_sys_htm(htm, seq=0):
    id = gid()
    bs = BuzzSys(id=id, htm=htm, seq=seq)
    bs.save()
    if seq:
        mc_buzz_sys_init_id_list.delete('')
#    from buzz import mq_buzz_sys_new_all
#    mq_buzz_sys_new_all(id)

def buzz_sys_edit(id, htm, seq):
    bs = BuzzSys.mc_get(id)
    if bs:
        bs.htm = htm
        seq = int(seq)
        seqchange = seq != bs.seq
        if seqchange:
            bs.seq = seq
        bs.save()
        if seqchange:
            mc_buzz_sys_init_id_list.delete('')

if __name__ == '__main__':
    pass
