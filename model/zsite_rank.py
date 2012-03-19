#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McCache
from kv import Kv
from zweb.orm import ormiter
from zsite_uv_daily import ZsiteUvDaily
from kv_misc import kv_int, KV_ZSITE_RANK_POWER
from model.zsite import Zsite, ZSITE_STATE_CAN_REPLY
from model.career import career_current
from model.ico import ico

class ZsiteRank(Model):
    pass


zsite_rank = Kv('zsite_rank', 0)

zsite_rank_get = zsite_rank.get
zsite_rank_set = zsite_rank.set

mc_zsite_rank_max = McCache('ZsiteRankMax.%s')

@mc_zsite_rank_max('{offset}')
def zsite_rank_max(offset=1):
    c = ZsiteRank.raw_sql('select value from zsite_rank order by value desc limit 1 offset %s', offset)
    return c.fetchone()[0] or 0


def zsite_rank_rebase():
    n = kv_int.get(KV_ZSITE_RANK_POWER) or 100
    if n > 5000:
        kv_int.set(KV_ZSITE_RANK_POWER, 100)
        ZsiteRank.raw_sql('update zsite_rank set value=value*100/%s', n)
        for i in ormiter(ZsiteRank):
            zsite_rank.mc_flush(i.id)
        mc_zsite_rank_max.delete('')


def zsite_rank_update_by_zsite_id(zsite_id, value_rank):
    ZsiteRank.raw_sql('insert into zsite_rank (id, value) values (%s, %s) on duplicate key update value=value+%s', zsite_id, value_rank, value_rank)
    zsite_rank.mc_flush(zsite_id)


def zsite_rank_update(days):
    n = kv_int.get(KV_ZSITE_RANK_POWER) or 100

    for i in ormiter(ZsiteUvDaily, 'days=%s' % days):
        zsite_id = i.zsite_id
        zsite_rank_update_by_zsite_id(zsite_id, i.uv*n)
    mc_zsite_rank_max.delete('')
    kv_int.set(KV_ZSITE_RANK_POWER, n*1.1)


def zsite_rank_by_zsite(zsite):
    from model.zsite_show import zsite_show_get
    rank = 0
    id = zsite.id
    if zsite.state > ZSITE_STATE_CAN_REPLY:
        rank += 3
        if zsite_show_get(id):
            rank += 1
    else:
        if career_current(id):
            rank += 1
        if ico.get(id):
            rank += 1
    return rank


def zsite_rank_by_zsite_id(id):
    return zsite_rank_by_zsite(Zsite.mc_get(id))



if __name__ == '__main__':
    #ZsiteRank.where().update(value=0)

    print zsite_rank_max(1)
    print zsite_rank_max(8)
