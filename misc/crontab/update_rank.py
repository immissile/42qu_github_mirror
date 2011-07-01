import init_env
from zweb.orm import ormiter
from model._db import Model
from user_rank import ZsiteUvDaily
from model.days import today_days

class KvInt(Model):
    pass

def update_user_rank():
    for i in ormiter(ZsiteUvDaily,"days=%s"%(today_days()-1)):
        today_rank = i.uv*power
        value = KvInt.raw_sql("select value from kv_int\
                                  where id=%s"%i.zsite_id).fetchone()[0]
        if value_item: 
            value_item = data_item * power + today_rank
            KvInt.raw_sql("update kv_int set value=%s where\
                      zsite_id = %s;"%(value_rank, i.zsite_id))
        else:
            KvInt.raw_sql("insert into kv_int (id, value) values\
                        (%s, %s)"%(i.zsite_id, value_rank))

if __name__=="__main__":
    update_user_rank()


