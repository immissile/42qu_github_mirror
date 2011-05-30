#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cid import CID_USER
from _db import Model, McModel

STATE_BAN = 1
STATE_DEL = 3
STATE_TO_VERIFY = STATE_RECALLED = 4
STATE_APPLY = 5
STATE_APPLYED = 7
STATE_ACTIVE = 10
STATE_VERIFY = 15
STATE_TODO = 17
STATE_REAL = 20

#ZPAGE_NAME = "主页"
#
#ZPAGE_STATE_INDEX = 10


class Zsite(McModel):
    pass

#
#class Zpage(McModel):
#    pass
#

def zsite_new(name, cid):
    zsite = Zsite(cid=cid, name=name, state=STATE_APPLY)
    zsite.save()
#    page = Zpage(
#        zsite_id=zsite.id,
#        name=ZPAGE_NAME,
#        state=ZPAGE_STATE_INDEX
#    )
#    page.save()
    return zsite

def zsite_new_user(name):
    return zsite_new(name, CID_USER)

if __name__ == "__main__":
    for i in Zsite.where():
        for reply in i.reply_list():
            print reply.html
