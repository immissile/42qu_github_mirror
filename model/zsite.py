#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _const import TID_ZSITE
from _db import Model, McModel
from reply import ReplyMixin,REPLY_STATE_ACTIVE,REPLY_STATE_SECRET

ZSITE_CID_USER = 1

ZSITE_STATE_DEFAULT = 20

#ZPAGE_NAME = "主页"
#
#ZPAGE_STATE_INDEX = 10


class Zsite(McModel, ReplyMixin):
    TID = TID_ZSITE


#
#class Zpage(McModel):
#    pass
#

def zsite_new(name, cid):
    zsite = Zsite(cid=cid, name=name, state=ZSITE_STATE_DEFAULT)
    zsite.save()
#    page = Zpage(
#        zsite_id=zsite.id,
#        name=ZPAGE_NAME,
#        state=ZPAGE_STATE_INDEX
#    )
#    page.save()
    return zsite

def zsite_new_user(name):
    return zsite_new(name, ZSITE_CID_USER)

if __name__ == "__main__":
    for i in Zsite.where():
        for reply in i.reply_list():
            print reply.html
