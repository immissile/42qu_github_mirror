#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cid import CID_USER
from _db import Model, McModel
from reply import ReplyMixin, STATE_ACTIVE, STATE_SECRET

ZSITE_BAN = 1
ZSITE_NO_MAIL = 5
ZSITE_APPLY = 9
ZSITE_SILENT = 13
ZSITE_ACTIVE = 17
ZSITE_VERIFY = 21

#ZPAGE_NAME = "主页"
#
#ZPAGE_STATE_INDEX = 10


class Zsite(McModel, ReplyMixin):
    pass

#
#class Zpage(McModel):
#    pass
#

def zsite_new(name, cid, state):
    zsite = Zsite(cid=cid, name=name, state=state)
    zsite.save()
#    page = Zpage(
#        zsite_id=zsite.id,
#        name=ZPAGE_NAME,
#        state=ZPAGE_STATE_INDEX
#    )
#    page.save()
    return zsite

def zsite_new_user(name):
    return zsite_new(name, CID_USER, ZSITE_APPLY)

if __name__ == "__main__":
    for i in Zsite.where():
        for reply in i.reply_list():
            print reply.html
