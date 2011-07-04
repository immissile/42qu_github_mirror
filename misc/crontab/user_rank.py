import init_env
from config import SITE_DOMAIN
from collections import defaultdict
#from model.zsite import Zsite
from model.user_session import user_id_by_base64
from model.zsite_url import id_by_url as _id_by_url
from model.days import  today_days
from model._db import Model

SUFFIX_LEN = len(SITE_DOMAIN)+1

class ZsiteUvDaily(Model):
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
    for uid, zid in log2zsite_id_user_id(LOG_FILE_PATH):
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


if __name__ == '__main__':
    LOG_FILE_PATH = '/var/log/nginx_backup/silegon_xxx_main.access_log.lzma'
    TODAY_DAYS = today_days()
    log2zsite_uv_daliy(TODAY_DAYS, LOG_FILE_PATH)

