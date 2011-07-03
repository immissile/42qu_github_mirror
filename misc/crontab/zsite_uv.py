import init_env
import subprocess
from zweb.orm import ormiter
from config import SITE_DOMAIN
from collections import defaultdict
#from model.zsite import Zsite
from model.zsite import Zsite
from model.user_session import user_id_by_base64
from model.zsite_link import id_by_url as _id_by_url
from model.days import  today_days
from model._db import Model
from model.kv_misc import kv_int , KV_ZSITE_RANK_POWER

SUFFIX_LEN = len(SITE_DOMAIN)+1

class ZsiteUvDaily(Model):
    pass

class ZsiteRank(Model):
    pass

def log2zsite_id_user_id(path):
    with open(path) as infile:
        for log in infile:
            user_id_base64, domain, other = log.split(' ', 2)
            url = domain[:-SUFFIX_LEN]
            if url and user_id_base64 != '-':
                yield id_by_url(url), user_id_by_base64(user_id_base64),

cache = {}
def id_by_url(url):
    if url.isdigit():
        return url
    if url not in cache:
        cache[url] = _id_by_url(url)
    return cache[url]


def log2zsite_id_uv(path):
    zsite_uv = defaultdict(set)
    for uid, zid in log2zsite_id_user_id(path):
        zsite_uv[zid].add(uid)
    return (
               (k, len(v)) for k, v in zsite_uv.iteritems()
           )


def log2zsite_uv_daliy(days, path):
    for zsite_id, uv in log2zsite_id_uv(path):
        ZsiteUvDaily.raw_sql(
            'insert into zsite_uv_daily (zsite_id, days, uv) values (%s, %s, %s) on duplicate key update uv=%s',
            zsite_id,
            days,
            uv,
            uv,
        )
####
def update_user_rank():
    power = kv_int.get(KV_ZSITE_RANK_POWER) or 1
    for i in ormiter(
        ZsiteUvDaily, "days=%s"%(today_days()-1)
    ):
        value_rank = i.uv*power
        i.raw_sql(" insert into zsite_rank (id, rank) values (%s, %s) on duplicate key update rank=rank+%s;"%(i.zsite_id, value_rank, value_rank))


def rebase_rank():
    max_rank = UserRank.raw_sql("select max(rank) from user_rank").fetchone()[0]
    if max_rank > 99:
        power = kv_int.get(KV_ZSITE_RANK_POWER) or 1
        ratio = power**30
        for i in ormiter(
            ZsiteRank
        ):
            i.raw_sql(" update zsite_rank set rank = rank/%s;"%ratio)


if __name__ == '__main__':
    LOG_FILE_PATH = '/var/log/nginx_backup/silegon_xxx_main.access_log.lzma'
    TODAY_DAYS = today_days()
    log2zsite_uv_daliy(TODAY_DAYS, LOG_FILE_PATH)
    pipe = subprocess.Popen(['cat'], stdout=subprocess.PIPE, ).stdout
    log2zsite_uv_daliy(TODAY_DAYS, pipe)
    pipe.close()
    update_user_rank()
    power = kv_int.get(KV_ZSITE_RANK_POWER) or 1
    if kv_int.value > 99:
        rebase_rank()
