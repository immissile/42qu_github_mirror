#!/usr/bin/env python
# -*- coding: utf-8 

from ctrl._urlmap.j import urlmap
from _handler import JLoginBase, Base
from model.buzz import Buzz,buzz_set_read, clear_buzz_by_po_id, clear_buzz_by_user_id_cid
from model.cid import CID_BUZZ_SYS, CID_BUZZ_SHOW, CID_BUZZ_FOLLOW, CID_BUZZ_WALL, CID_BUZZ_WALL_REPLY, CID_BUZZ_PO_REPLY, CID_BUZZ_ANSWER, CID_BUZZ_JOIN, CID_BUZZ_EVENT_JOIN_APPLY, CID_BUZZ_EVENT_FEEDBACK_JOINER, CID_BUZZ_EVENT_FEEDBACK_OWNER, CID_USER, CID_BUZZ_SITE_NEW , CID_BUZZ_SITE_FAV, CID_BUZZ_WORD
from model.po import Po, PO_SHARE_FAV_CID
from json import dumps


CID_EVENT=[
        CID_BUZZ_EVENT_JOIN_APPLY,
        CID_BUZZ_EVENT_FEEDBACK_JOINER,
        CID_BUZZ_EVENT_FEEDBACK_JOINER
        ]

CID_FOLLOW=[
        CID_BUZZ_FOLLOW,
        CID_BUZZ_SITE_NEW,
        CID_BUZZ_SITE_FAV,
        CID_BUZZ_JOIN,
        ]

CID_REPLY=[
        CID_BUZZ_PO_REPLY,
        CID_BUZZ_ANSWER,
        ]

CID_DICT={
        0:CID_EVENT,
        1:CID_FOLLOW,
        2:CID_REPLY
        }

@urlmap('/j/reply/rm/(0|1)/(\d+)')
class PoReplyJson(JLoginBase):
    def post(self, state, id):
        current_user_id = self.current_user_id
        clear_buzz_by_po_id(current_user_id,id)
        state = int(state)
        if state:
            out = ['ok']
        else:
            out = ['fal']
        self.finish(dumps(out))

@urlmap('/j/buzz/clean/(\d+)')
class PoClean(JLoginBase):
    def get(self,id):
        current_user_id = self.current_user_id
        if id:
            id = int(id)
            for cid in CID_DICT[id]: 
                clear_buzz_by_user_id_cid(current_user_id,cid)
        self.finish("{}")


