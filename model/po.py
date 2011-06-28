#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache, McNum
from cid import CID_WORD, CID_NOTE, CID_QUESTION
from feed import feed_new, mc_feed_tuple, feed_rm
from gid import gid
from spammer import is_same_post
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get, txt_property
from zkit.time_format import time_title
from reply import ReplyMixin
from po_pic import pic_htm
from zkit.txt2htm import txt_withlink
from zsite import Zsite
from zkit.txt import cnencut
from cgi import escape

PO_EN = {
    CID_NOTE: 'note',
    CID_WORD: 'word',
    CID_QUESTION: 'question',
}

mc_htm = McCache('PoHtm.%s')

class Po(McModel, ReplyMixin):

    @property
    def txt(self):
        if self.cid == CID_WORD:
            return self.name_
        else:
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

    @property
    def question(self):
        if not hasattr(self, '_question'):
            self._question = Po.mc_get(self.rid)
        return self._question

    @property
    def name(self):
        if self.cid == CID_NOTE:
            q = self.question
            if q:
                return '答：%s' % q.name
        return self.name_

    @property
    def name_htm(self):
        q = self.question
        if q:
            return '答：<a href="%s">%s</a>' % (q.link, escape(q.name))
        return escape(self.name)

    def txt_set(self, txt):
        id = self.id
        txt_new(id, txt)
        mc_htm.delete(id)

    @property
    def link(self):
        if not hasattr(self, '_link'):
            zsite = Zsite.mc_get(self.user_id)
            self._link = '%s/%s' % (zsite.link, self.id)
        return self._link
    
    @property
    def user(self):
        self.__dict__['user'] = user = Zsite.mc_get(self.user_id)
        return user

    @property
    def link_reply(self):
        if self.cid == CID_QUESTION:
            zsite = Zsite.mc_get(self.user_id)
            return  '%s/question/%s' % (zsite.link, self.id)
        return self.link

    @property
    def link_edit(self):
        if not hasattr(self, '_link_edit'):
#            en = PO_EN[self.cid]
            zsite = Zsite.mc_get(self.user_id)
            self._link_edit = '%s/po/edit/%s' % (zsite.link, self.id)
        return self._link_edit

    def feed_new(self):
        feed_new(self.id, self.user_id, self.cid)

    def can_view(self, user_id):
        if self.state <= STATE_DEL:
            return False
        if self.state == STATE_SECRET:
            if (not user_id) or ( self.user_id != user_id ):
                return False
        return True

    def can_admin(self, user_id):
        return self.user_id == user_id

    def reply_new(self, user, txt, state=STATE_ACTIVE):
        result = super(Po, self).reply_new(user, txt, state)
        mc_feed_tuple.delete(self.id)
        return result

def po_new(cid, user_id, name, rid, state):
    m = Po(
        id=gid(),
        name_=cnencut(name, 140),
        user_id=user_id,
        cid=cid,
        rid=rid,
        state=state,
        create_time=int(time()),
    )
    m.save()
    mc_flush(user_id)
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
    mc_flush_other(po.user_id)

def po_rm(user_id, id):
    m = Po.mc_get(id)
    if m.can_admin(user_id):
        m.state = STATE_DEL
        m.save()
        feed_rm(id)
        from zsite_tag import zsite_tag_rm_by_po_id
        zsite_tag_rm_by_po_id(id)
        from rank import rank_rm_all
        rank_rm_all(id)
        from po_question import mc_answer_id_get
        rid = m.rid
        if rid:
            mc_answer_id_get.delete('%s_%s' % (user_id, rid))
        mc_flush(user_id)
        return True

def po_word_new(user_id, name, state=STATE_ACTIVE, rid=0):
    if name and not is_same_post(user_id, name):
        m = po_new(CID_WORD, user_id, name, rid, state)
        if state > STATE_SECRET:
            m.feed_new()
        return m

def po_note_new(user_id, name, txt, state, rid=0):
    if not txt and not name:
        return
    name = name or time_title()
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_NOTE, user_id, name, rid, state)
        txt_new(m.id, txt)
        if state > STATE_SECRET:
            m.feed_new()
        return m

PO_LIST_STATE = {
    True: 'state>%s' % STATE_DEL,
    False: 'state>%s' % STATE_SECRET,
}

po_list_count = McNum(lambda user_id, is_self: Po.where(user_id=user_id).where(PO_LIST_STATE[is_self]).count(), 'PoListCount.%s')

mc_po_id_list = McLimitA('PoIdList.%s', 512)

@mc_po_id_list('{user_id}_{is_self}')
def po_id_list(user_id, is_self, limit, offset):
    return Po.where(user_id=user_id).where(PO_LIST_STATE[is_self]).order_by('id desc').col_list(limit, offset)

def po_view_list(user_id, is_self, limit, offset):
    return Po.mc_get_list(po_id_list(user_id, is_self, limit, offset))

def mc_flush(user_id):
    mc_flush_other(user_id)
    mc_flush_self(user_id)

def _mc_flush(user_id, is_self):
    key = '%s_%s' % (user_id, is_self)
    po_list_count.delete(key)
    mc_po_id_list.delete(key)

def mc_flush_self(user_id):
    _mc_flush(user_id, True)

def mc_flush_other(user_id):
    _mc_flush(user_id, False)

if __name__ == '__main__':
    pass
