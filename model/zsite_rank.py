#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McCache
from kv import Kv
from zweb.orm import ormiter
from zsite_uv_daily import ZsiteUvDaily
from days import today_days
from kv_misc import kv_int, KV_ZSITE_RANK_POWER


class ZsiteRank(Model):
    pass


zsite_rank = Kv('zsite_rank', 0)

zsite_rank_get = zsite_rank.get
zsite_rank_set = zsite_rank.set

mc_zsite_rank_max = McCache('ZsiteRankMax.%s')

@mc_zsite_rank_max('')
def zsite_rank_max():
    c = ZsiteRank.raw_sql('select max(value) from zsite_rank')
    return c.fetchone()[0]

def zsite_rank_rebase():
    n = kv_int.get(KV_ZSITE_RANK_POWER) or 100
    if n > 9999:
        kv_int.set(KV_ZSITE_RANK_POWER, 100)
        ZsiteRank.raw_sql('update zsite_rank set value=value*100/%s', n)
        for i in ormiter(ZsiteRank):
            zsite_rank.mc_flush(i.id)
        mc_zsite_rank_max.delete('')

def zsite_rank_update(days):
    n = kv_int.get(KV_ZSITE_RANK_POWER) or 100

    for i in ormiter(ZsiteUvDaily, 'days=%s' % days):
        zsite_id = i.zsite_id
        value_rank = i.uv * n
        i.raw_sql('insert into zsite_rank (id, value) values (%s, %s) on duplicate key update value=value+%s', zsite_id, value_rank, value_rank)
        zsite_rank.mc_flush(zsite_id)

    mc_zsite_rank_max.delete('')
    kv_int.set(KV_ZSITE_RANK_POWER, n*1.1)
