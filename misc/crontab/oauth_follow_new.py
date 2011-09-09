#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.kv_misc import kv_int, KV_OAUTH_FOLLOW
from model.oauth import OauthToken
from model.oauth_follow import oauth_follow_by_oauth_id


@single_process
def oauth_follow():
    rss_pos = kv_int.get(KV_OAUTH_FOLLOW)
    c = OauthToken.raw_sql('select max(id) from oauth_token')
    pos = c.fetchone()[0]
    if pos > rss_pos:
        c = OauthToken.raw_sql('select id from oauth_token where id>%s and id<=%s order by id',rss_pos,pos)
        for id, in c.fetchall():
            #print id
            #import sys
            #sys.stdout.flush()
            oauth_follow_by_oauth_id(id)
        kv_int.set(KV_OAUTH_FOLLOW, pos)


if __name__ == "__main__":
    oauth_follow()
