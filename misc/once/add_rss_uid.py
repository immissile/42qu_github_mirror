#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import _env
from model.rss import Rss

def get_uid():
    with open('uid_url') as x:
        x = x.readlines()
        uids = []
        for i in x:
            i = i.strip()
            i = i.split('!!')
            uids.append(i)
        return uids

def add_rss(uids):
    for i in uids:
        Rss.raw_sql('insert into rss (user_id,url,gid) values(%s,%s,0)', i[0], i[1])


if __name__ == '__main__':
    add_rss(get_uid())
