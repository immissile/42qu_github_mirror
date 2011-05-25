#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache, McTotal
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER
from feed import feed_entry_new, mc_feed_entry_tuple, feed_entry_rm
from gid import gid
from pic import pic_new, pic_save
from spammer import is_same_post
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get
from zkit.time_format import time_title
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from reply import ReplyMixin

PO_LINK = {
    CID_NOTE : '/note/%s',
    CID_WORD : '/word/%s',
}

class Po(McModel, ReplyMixin):
    @property
    def txt(self):
        return txt_get(self.id)

    @property
    def link(self):
        if not hasattr(self, '_link'):
            self._link = PO_LINK[self.cid]%self.id
        return self._link

    def can_admin(self, user_id):
        return self.user_id == user_id

    def feed_entry_new(self):
        feed_entry_new(self.id, self.user_id, self.cid)

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
        return (m.name, m.txt)
    return ()

@mc_feed_entry_tuple('{id}')
def feed_tuple_word(id):
    m = Po.mc_get(id)
    if m:
        return (m.name, )
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

def po_note_can_view(po, user_id):
    if not po:
        return False
    if po.state <= STATE_DEL:
        return False
    if po.cid != CID_NOTE:
        return False
    if po.state == STATE_SECRET:
        if po.user_id != user_id:
            return False
    return True

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

class PoPic(McModel):
    pass

def pic_id_list(po_id):
    return PoPic.where(po_id=po_id).order_by('seq desc').id_list()

def pic_new_id_list(user_id):
    return PoPic.where(user_id=user_id, po_id=0).order_by('seq desc').id_list()

po_pic_total = McTotal(lambda user_id, po_id: PoPic.where(user_id=user_id, po_id=po_id).count(), 'PoPicTotal.%s')

def can_new_pic(user_id, po_id=0):
    return po_pic_total(user_id, po_id) < PIC_LIMIT
#po_pic_seq = McTotal(
def new_pic_seq(user_id, po_id):
    c = PoPic.raw_sql('select max(seq) from po_pic where user_id=%s and po_id=%s', user_id, po_id)
    seq = c.fetchone()[0] or 0
    return seq + 1

if __name__ == '__main__':
    pass
