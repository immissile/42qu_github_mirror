#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from feed import feed_entry_new, mc_feed_entry_tuple, feed_entry_rm
from gid import gid
from spammer import is_same_post
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zkit.time_format import time_title
from reply import ReplyMixin
from po_pic import pic_htm, pic_seq_dic
from zkit.txt import txt_withlink

PO_LINK = {
    CID_NOTE: '/note/%s',
    CID_WORD: '/word/%s',
}

mc_htm = McCache('PoHtm.%s')

class Po(McModel, ReplyMixin):
    @property
    def txt(self):
        return txt_get(self.id)

    @property
    @mc_htm('{self.id}')
    def htm(self):
        txt = txt_withlink(self.txt)
        return pic_htm(txt, pic_seq_dic(self.user_id, self.id))

    def txt_set(self, txt):
        id = self.id
        txt_new(id, txt)
        mc_htm.delete(id)

    @property
    def link(self):
        if not hasattr(self, '_link'):
            self._link = PO_LINK[self.cid]%self.id
        return self._link

    def feed_entry_new(self):
        feed_entry_new(self.id, self.user_id, self.cid)

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
        mc_feed_entry_tuple.delete(self.id)
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
        feed_entry_rm(id)
    elif old_state <= STATE_SECRET and state >= STATE_ACTIVE:
        po.feed_entry_new()
    po.state = state
    po.save()

def po_rm(user_id, id):
    m = Po.mc_get(id)
    if m.can_admin(user_id):
        m.state == STATE_DEL
        m.save()
        feed_entry_rm(id)

@mc_feed_entry_tuple('{id}')
def feed_tuple_note(id):
    m = Po.mc_get(id)
    if m:
        return (m.name, m.txt, m.reply_total)
    return ()

@mc_feed_entry_tuple('{id}')
def feed_tuple_word(id):
    m = Po.mc_get(id)
    if m:
        return (m.name, m.reply_total)
    return False

def po_word_new(user_id, name):
    if name and not is_same_post(user_id, name):
        m = po_new(CID_WORD, user_id, name, STATE_ACTIVE)
        id = m.id
        m.feed_entry_new()
        return m

#def po_question_new(user_id, name , txt):
#    m = po_new(CID_QUESTION, user_id, name, STATE_SECRET)
#    txt_new(m.id, txt)
#    return m


def po_note_new(user_id, name, txt, state):
    name = name or time_title()
    if is_same_post(user_id, name, txt):
        return
    m = po_new(CID_NOTE, user_id, name, state)
    id = m.id
    txt_new(id, txt)
    if state > STATE_SECRET:
        m.feed_entry_new()
    return m

if __name__ == '__main__':
    pass
