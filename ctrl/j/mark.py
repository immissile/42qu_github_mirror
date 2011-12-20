#!/usr/bin/env python
# -*- coding: utf-8 

from ctrl._urlmap.j import urlmap
from _handler import JLoginBase, Base
from model.buzz import Buzz,buzz_set_read, clear_buzz_by_po_id
from model.cid import CID_BUZZ_SYS, CID_BUZZ_SHOW, CID_BUZZ_FOLLOW, CID_BUZZ_WALL, CID_BUZZ_WALL_REPLY, CID_BUZZ_PO_REPLY, CID_BUZZ_ANSWER, CID_BUZZ_JOIN, CID_BUZZ_EVENT_JOIN_APPLY, CID_BUZZ_EVENT_FEEDBACK_JOINER, CID_BUZZ_EVENT_FEEDBACK_OWNER, CID_USER, CID_BUZZ_SITE_NEW , CID_BUZZ_SITE_FAV, CID_BUZZ_WORD
from model.po import Po, PO_SHARE_FAV_CID

@urlmap('/j/reply/rm/(\d+)')
class PoReplyJson(JLoginBase):
    def get(self, id):
        current_user_id = self.current_user_id
        clear_buzz_by_po_id(current_user_id,id)

