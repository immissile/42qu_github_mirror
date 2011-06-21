#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cid import CID_USER
from _db import Model, McModel
from gid import gid

ZSITE_STATE_BAN = 1
ZSITE_STATE_NO_MAIL = 5
ZSITE_STATE_APPLY = 10
ZSITE_STATE_ACTIVE = 15
ZSITE_STATE_FAILED_VERIFY = 20
ZSITE_STATE_WAIT_VERIFY = 25
ZSITE_STATE_VERIFY_CANNOT_REPLY = 30
ZSITE_STATE_CAN_REPLY = 35
ZSITE_STATE_VERIFY = 40

#ZPAGE_NAME = "主页"
#
#ZPAGE_STATE_INDEX = 10


class Zsite(McModel):
    pass

def user_can_reply(user):
    return user.state >= ZSITE_STATE_CAN_REPLY
#
#class Zpage(McModel):
#    pass
#

def zsite_new(name, cid, state):
    zsite = Zsite(id=gid(), cid=cid, name=name, state=state)
    zsite.save()
#    page = Zpage(
#        zsite_id=zsite.id,
#        name=ZPAGE_NAME,
#        state=ZPAGE_STATE_INDEX
#    )
#    page.save()
    return zsite

def zsite_new_user(name):
    return zsite_new(name, CID_USER, ZSITE_STATE_APPLY)

if __name__ == '__main__':
    pass
# for i in Zsite.where():
#     for reply in i.reply_list():
#         print reply.html



