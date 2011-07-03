from model._db import Model
from zweb.orm import ormiter
from user_rank import ZsiteUvDaily
from model.days import today_days
from model.kv_misc import kv_int , KV_ZSITE_RANK_POWER

class ZsiteRank(Model):
    pass




def rank_rebase():
    power = kv_int.get(KV_ZSITE_RANK_POWER) or 1

    ZsiteRank.raw_sql(" update zsite_rank set rank = rank/%s", power)

    kv_int.set(KV_ZSITE_RANK_POWER, 1)



def rank_update():

    power = kv_int.get(KV_ZSITE_RANK_POWER) or 1

    for i in ormiter(
        ZsiteUvDaily, 'days=%s'%(today_days()-1)
    ):
        value_rank = int(i.uv*power)
        i.raw_sql('insert into zsite_rank (id, rank) values (%s, %s) on duplicate key update rank = rank + %s', i.zsite_id, value_rank, value_rank)

    kv_int.set(KV_ZSITE_RANK_POWER, power*1.1)

