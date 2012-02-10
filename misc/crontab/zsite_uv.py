#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
import subprocess
from zweb.orm import ormiter
from config import SITE_DOMAIN
from collections import defaultdict
from model.zsite import Zsite
from model.zsite_uv_daily import ZsiteUvDaily
from model.user_session import user_id_by_base64
from model.zsite_url import id_by_url as _id_by_url
from model.days import date_to_days, yesterday

SUFFIX_LEN = len(SITE_DOMAIN)+1


def log2zsite_id_user_id(f):
    for log in f:
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


def log2zsite_id_uv(f):
    zsite_uv = defaultdict(set)
    for zid, uid in log2zsite_id_user_id(f):
        zsite_uv[zid].add(uid)
    for k, v in zsite_uv.iteritems():
        yield k, len(v)


def log2zsite_uv_daliy(days, f):
    for zsite_id, uv in log2zsite_id_uv(f):
        if not Zsite.mc_get(zsite_id):
            continue
        ZsiteUvDaily.raw_sql(
            'insert into zsite_uv_daily (zsite_id, days, uv) values (%s, %s, %s) on duplicate key update uv=%s',
            zsite_id,
            days,
            uv,
            uv,
        )

def log_parser(date):
    from model.zsite_rank import zsite_rank_rebase, zsite_rank_update
    from model.zsite_show import zsite_show_update
    from config import NGINX_LOGROTATE_DIR
    from os.path import join
    filepath = join(
        NGINX_LOGROTATE_DIR,
        '%s_zsite.access_log-%s.lzma'%(SITE_DOMAIN.replace('.', '_'), date)
    )
    #print filepath
    pipe = subprocess.Popen(['lzcat', filepath], stdout=subprocess.PIPE, ).stdout
    days = date_to_days(date)
    log2zsite_uv_daliy(days, pipe)
    pipe.close()
    zsite_rank_update(days)
    zsite_rank_rebase()
    zsite_show_update()


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1:
        date = sys.argv[1]
    else:
        date = yesterday()

    log_parser(date)

