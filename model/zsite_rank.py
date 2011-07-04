#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model
from zweb.orm import ormiter
from zsite_uv_daily import ZsiteUvDaily
from days import today_days
from kv_misc import kv_int, KV_ZSITE_RANK_POWER


class ZsiteRank(Model):
    pass


def zsite_rank_get(id):
    o = ZsiteRank.get(id)
    if o:
        return o.rank
    return 0

def zsite_rank_max():
    c = ZsiteRank.raw_sql('select max(rank) from zsite_rank')
    return c.fetchone()[0]

def zsite_rank_rebase():
    n = kv_int.get(KV_ZSITE_RANK_POWER) or 100
    if n > 9999:
        kv_int.set(KV_ZSITE_RANK_POWER, 100)
        ZsiteRank.raw_sql('update zsite_rank set rank=rank/%s', n)

def zsite_rank_update(days):
    n = kv_int.get(KV_ZSITE_RANK_POWER) or 100

    for i in ormiter(ZsiteUvDaily, 'days=%s' % days):
        value_rank = i.uv*n
        i.raw_sql('insert into zsite_rank (id, rank) values (%s, %s) on duplicate key update rank=rank+%s;'%(i.zsite_id, value_rank, value_rank))

    kv_int.set(KV_ZSITE_RANK_POWER, n*1.1)
