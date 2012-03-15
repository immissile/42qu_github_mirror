#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from collections import defaultdict
from mmseg.search import seg_txt_search, seg_title_search, seg_txt_2_dict
from zweb.orm import ormiter
from model.career import career_list_all
from model.txt import txt_get
from model.user_mail import mail_by_user_id
from model.zsite import Zsite, CID_USER, ZSITE_STATE_CAN_REPLY
from model.zsite_url import url_by_id
from model.zsite_rank import zsite_rank_by_zsite_id
from model.search_zsite import SearchZsite
from model.cid import CID_SITE
from model.motto import motto_get

def zsite2keyword(z):
    r = []
    t = defaultdict(int)
    id = z.id

    name = z.name
    if name:
        for word in seg_title_search(name):
            t[word] += 2

    url = url_by_id(id)
    if url:
        t[url] += 2

    if z.cid == CID_SITE:
        for word in seg_title_search(motto_get(id)):
            t[word] += 1

    elif z.cid == CID_USER:

        mail = mail_by_user_id(id)
        if mail:
            t[mail] += 2
            t[mail.split('@', 1)[0]] += 2


        txt = txt_get(id)

        if txt:
            man_txt_len = len(txt)

            for word in seg_txt_search(txt):
                t[word] += 1

        for seq, career in enumerate(career_list_all(id)):
            if seq:
                add = 1
            else:
                add = 2

            unit = career.unit
            title = career.title
            txt = career.txt

            if unit:
                for word in seg_title_search(unit):
                    t[word] += add

            if title:
                for word in seg_title_search(title):
                    t[word] += add
            if txt:
                for word in seg_txt_search(txt):
                    t[word] += add

    return t



def search_zsite_keyword_iter():
    for i in ormiter(SearchZsite):
        id = i.id
        i.delete()
        zsite = Zsite.mc_get(id)
        if zsite and zsite.state:
            kw = zsite2keyword(zsite)
            if kw:
                yield zsite_keyword(zsite, kw)



def zsite_keyword_iter():
    for zsite in ormiter(Zsite, 'state>0'):
        kw = zsite2keyword(zsite)
        if kw:
            yield zsite_keyword(zsite, kw)


def zsite_keyword(zsite, kw):
    id = zsite.id
    return str(id), str(zsite.cid), zsite_rank_by_zsite_id(id), kw.items()



if __name__ == '__main__':
#    for i in search_zsite_keyword_iter():
#        print i
    from model.zsite import Zsite
    for i in zsite2keyword(Zsite.mc_get(10078835)):
        print i
