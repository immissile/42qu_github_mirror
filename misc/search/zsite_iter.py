#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from model.zsite import Zsite, CID_USER, ZSITE_STATE_CAN_REPLY
from model.txt import txt_get
from model.user_mail import mail_by_user_id
from model.zsite_list_0 import zsite_show_get
from zweb.orm import ormiter
from mmseg.search import seg_txt_search, seg_title_search, seg_txt_2_dict
from collections import defaultdict


def zsite2keyword(z):
    rank = 0
    r = []
    t = defaultdict(int)
    id = z.id
    if z.cid == CID_USER:
        mail = mail_by_user_id(id)
        if mail:
            t[mail] += 2
            t[mail.split('@')[0]] += 2

    name = z.name
    if name:
        for word in seg_title_search(name):
            t[word] += 2

    txt = txt_get(id)

    if txt:
        man_txt_len = len(txt)
        if man_txt_len > 100:
            rank += 5
        else:
            rank += 1

        for word in seg_title_search(txt):
            t[word] += 1

    return rank, t


def man_keyword_iter():
    for i in ormiter(Zsite):
        id = i.id
        rk = zsite2keyword(i)
        if not rk:
            continue
        rank, kw = rk
        if i.state > ZSITE_STATE_CAN_REPLY:
            rank += 100
        show = zsite_show_get(id)
        if show:
            rank += 100 * show.rank

        yield str(id), rank, kw.items()


if __name__ == '__main__':
    z = Zsite.mc_get(10000187)
    if z:
        for k, v in zsite2keyword(z)[1].iteritems():
            print k, v
