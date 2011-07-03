import init_env
from zweb.orm import ormiter
from model._db import Model
from model.kv_misc import kv_int , KV_ZSITE_RANK_POWER

class ZsiteRank(Model):
    pass

def rebase_rank():
    power = kv_int.get(KV_ZSITE_RANK_POWER) or 1
    ratio = power**30
    for i in ormiter(
        ZsiteRank
    ):
        i.raw_sql(" update zsite_rank set rank = rank/%s;"%ratio)

if __name__=="__main__":
    rebase_rank()


