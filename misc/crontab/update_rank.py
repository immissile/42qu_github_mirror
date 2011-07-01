import init_env
from zweb.orm import ormiter
from model._db import Model
from user_rank import ZsiteUvDaily
from model.days import today_days
from model.kv_misc import kv_int , KV_ZSITE_RANK_POWER

def ZsiteRank(Model):
    pass

def update_user_rank():
    power = kv_int.get(KV_ZSITE_RANK_POWER) or 1
    for i in ormiter(
        ZsiteUvDaily,"days=%s"%(today_days()-1)
    ):
        value_rank = i.uv*power
        i.raw_sql(" insert into zsite_rank (id, rank) values (%s, %s) on duplicate key update rank=rank+%s;"%(i.zsite_id, value_rank, value_rank))

if __name__=="__main__":
    update_user_rank()


