#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache, McNum
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PO
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
from zkit.attrcache import attrcache
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
        cid = self.cid
        if cid == CID_WORD:
            return self.name_
        elif cid == CID_ANSWER:
            return txt_get(self.id) or self.name_
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

    def txt_set(self, txt):
        id = self.id
        txt_new(id, txt)
        mc_htm.delete(id)

    @attrcache
    def user(self):
        return Zsite.mc_get(self.user_id)

    @attrcache
    def question(self):
        return Po.mc_get(self.rid)

    @attrcache
    def name(self):
        q = self.question
        if q:
            u = q.user
            return '答 : %s' % q.name
        if self.cid == CID_WORD:
            return ''
        return self.name_

    @attrcache
    def name_htm(self):
        q = self.question
        if q:
            u = q.user
            link = '<a href="%s">%s</a>' % (q.link, escape(q.name))
            if q.user_id == self.user_id:
                return '自问自答 : %s' % link
            return '答 <a href="%s">%s</a> 问 :' % (u.link, escape(u.name), link)
        if self.cid == CID_WORD:
            return ''
        return escape(self.name)

    @attrcache
    def link(self):
        u = self.user
        return '%s/%s' % (u.link, self.id)

    @attrcache
    def link_question(self):
        q = self.question
        if q:
            return '%s#reply%s' % (q.link, self.id)
        return self.link

    @attrcache
    def link_reply(self):
        if self.cid == CID_QUESTION:
            u = self.user
            return '%s/question/%s' % (u.link, self.id)
        return self.link

    @attrcache
    def link_edit(self):
        u = self.user
        return '%s/po/edit/%s' % (u.link, self.id)

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
    mc_flush(user_id, cid)
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

def po_cid_set(po, cid):
    o_cid = po.cid
    if cid != o_cid:
        po.cid = cid
        po.save()
        mc_flush_cid_mv(po.user_id, o_cid, cid)

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
        from po_question import mc_answer_id_get, answer_count
        rid = m.rid
        if rid:
            mc_answer_id_get.delete('%s_%s' % (user_id, rid))
            answer_count.delete(rid)
        mc_flush(user_id, m.cid)
        return True

def po_word_new(user_id, name, state=STATE_ACTIVE, rid=0):
    if name and not is_same_post(user_id, name):
        m = po_new(CID_WORD, user_id, name, rid, state)
        if state > STATE_SECRET:
            m.feed_new()
        return m

def po_note_new(user_id, name, txt, state, rid=0):
    if not name and not txt:
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


po_list_cid_count = McNum(lambda user_id, cid, is_self: Po.where(user_id=user_id, cid=cid).where(PO_LIST_STATE[is_self]).count(), 'PoListCount.%s')

mc_po_id_list_by_cid = McLimitA('PoIdListByCid.%s', 512)

@mc_po_id_list_by_cid('{user_id}_{cid}_{is_self}')
def po_id_list_by_cid(user_id, cid, is_self, limit, offset):
    return Po.where(user_id=user_id).where(PO_LIST_STATE[is_self]).order_by('id desc').col_list(limit, offset)

def po_view_list(user_id, cid, is_self, limit, offset):
    return Po.mc_get_list(po_id_list(user_id, cid, is_self, limit, offset))

def mc_flush_all(user_id):
    for is_self in (True, False):
        for cid in CID_PO:
            _mc_flush_cid(user_id, cid, is_self)
        _mc_flush_all(user_id, cid)

def mc_flush(user_id, cid):
    mc_flush_other(user_id, cid)
    mc_flush_self(user_id, cid)

def mc_flush_self(user_id, cid):
    _mc_flush(user_id, cid, True)

def mc_flush_other(user_id, cid):
    _mc_flush(user_id, cid, False)

def _mc_flush(user_id, cid, is_self):
    _mc_flush_all(user_id, is_self)
    _mc_flush_cid(user_id, cid, is_self)

def _mc_flush_all(user_id, is_self):
    key = '%s_%s' % (user_id, is_self)
    po_list_count.delete(key)
    mc_po_id_list.delete(key)

def _mc_flush_cid(user_id, is_self):
    key2 = '%s_%s_%s' % (user_id, cid, is_self)
    po_list_cid_count.delete(key2)
    mc_po_id_list_by_cid.delete(key2)

def mc_flush_cid_mv(user_id, cid1, cid2):
    for is_self in (True, False):
        _mc_flush_cid(user_id, cid1, is_self)
        _mc_flush_cid(user_id, cid2, is_self)

if __name__ == '__main__':
    pass
