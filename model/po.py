#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from feed import feed_new, mc_feed_tuple, feed_rm
from gid import gid
from spammer import is_same_post
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zkit.time_format import time_title
from reply import ReplyMixin
from po_pic import pic_htm
from zkit.txt2htm import txt_withlink
from zsite import Zsite

PO_EN = {
    CID_NOTE: 'note',
    CID_WORD: 'word',
    CID_QUESTION: 'question',
}

mc_htm = McCache('PoHtm.%s')

class Po(McModel, ReplyMixin):
    @property
    def txt(self):
        return txt_get(self.id)

    @property
    @mc_htm('{self.id}')
    def htm(self):
        cid = self.cid
        id = self.id
        h = txt_withlink(self.txt)
        if cid != CID_WORD:
            from po_pic import pic_htm
            user_id = self.user_id
            h = pic_htm(h, user_id, id)
        return h

    def txt_set(self, txt):
        id = self.id
        txt_new(id, txt)
        mc_htm.delete(id)

    @property
    def link(self):
        if self.cid not in PO_EN:
            return ''
        if not hasattr(self, '_link'):
            en = PO_EN[self.cid]
            zsite = Zsite.mc_get(self.user_id)
            link = '%s/%s/%s'%(zsite.link, en, self.id)
            self._link = link
        return self._link

    def feed_new(self):
        feed_new(self.id, self.user_id, self.cid)

    def can_view(self, user_id):
        if self.state <= STATE_DEL:
            return False
        if self.state == STATE_SECRET:
            if self.user_id != user_id:
                return False
        return True

    def can_admin(self, user_id):
        return self.user_id == user_id

    def reply_new(self, user_id, txt, state=STATE_ACTIVE):
        result = super(Po, self).reply_new(user_id, txt, state)
        mc_feed_tuple.delete(self.id)
        return result

def po_new(cid, user_id, name, state):
    m = Po(
        id=gid(),
        name=name,
        user_id=user_id,
        create_time=int(time()),
        cid=cid,
        state=state
    )
    m.save()
    return m

def po_state_set(po, state):
    old_state = po.state
    if old_state == state:
        return
    if old_state > STATE_SECRET and state == STATE_SECRET:
        feed_rm(id)
    elif old_state <= STATE_SECRET and state >= STATE_ACTIVE:
        po.feed_new()
    po.state = state
    po.save()

def po_rm(user_id, id):
    m = Po.mc_get(id)
    if m.can_admin(user_id):
        m.state == STATE_DEL
        m.save()
        feed_rm(id)

def po_word_new(user_id, name):
    if name and not is_same_post(user_id, name):
        m = po_new(CID_WORD, user_id, name, STATE_ACTIVE)
        m.feed_new()
        return m

def po_note_new(user_id, name, txt, state):
    name = name or time_title()
    if is_same_post(user_id, name, txt):
        return
    m = po_new(CID_NOTE, user_id, name, state)
    txt_new(m.id, txt)
    if state > STATE_SECRET:
        m.feed_new()
    return m

if __name__ == '__main__':
    pass
