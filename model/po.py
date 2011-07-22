#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache, McNum
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PO
from feed import feed_new, mc_feed_tuple, feed_rm
from feed_po import mc_feed_po_iter, mc_feed_po_dict
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

PO_CN_EN = (
    (CID_WORD, 'word', '微博', '句'),
    (CID_NOTE, 'note', '文章', '篇'),
    (CID_QUESTION, 'question', '问题', '条'),
    (CID_ANSWER, 'answer', '回答', '次'),
)
PO_EN = dict((i[0], i[1]) for i in PO_CN_EN)
PO_CN = dict((i[0], i[2]) for i in PO_CN_EN)
PO_COUNT_CN = dict((i[0], i[3]+i[2]) for i in PO_CN_EN)


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

    def mc_flush(self):
        if not hasattr(self, '_mc_flush'):
            if self._new_record:
                rid = self.rid
                if rid:
                    from model.po_question import answer_count
                    answer_count.delete(rid)
                    mc_feed_tuple.delete(rid)
            else:
                id = self.id
                mc_htm.delete(id)
                mc_feed_tuple.delete(id)
                mc_feed_po_dict.delete(id)
            self._mc_flush = True

    def save(self):
        self.mc_flush()
        super(Po, self).save()

    @property
    @mc_htm('{self.id}')
    def htm(self):
        cid = self.cid
        id = self.id
        s = txt_withlink(self.txt)
        if cid != CID_WORD:
            from po_pic import pic_htm
            user_id = self.user_id
            s = pic_htm(s, user_id, id)
            s = s.replace('\n\n', '</p><p>')
            s = '<p>%s</p>' % s
        return s

    def txt_set(self, txt):
        id = self.id
        txt_new(id, txt)
        self.mc_flush()

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
            return '答 : %s' % q.name
        #if self.cid == CID_WORD:
        #    return ''
        return self.name_

    @attrcache
    def name_with_user(self):
        q = self.question
        if q:
            u = self.user
            return '%s 答 : %s' % (u.name, q.name)
        return self.name_

    @attrcache
    def name_htm(self):
        q = self.question
        if q:
            u = q.user
            link = '<a href="%s">%s</a>' % (q.link, escape(q.name))
            if q.user_id == self.user_id:
                return '自问自答 : %s' % link
            return '答 <a href="%s">%s</a> 问 : %s' % (
                u.link, escape(u.name), link
            )
        if self.cid == CID_WORD:
            return txt_withlink(self.name)
        return escape(self.name)

    @attrcache
    def link(self):
        u = self.user
        #TODO REMOVE
        if u:
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

def po_new(cid, user_id, name, state, rid=0):
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
    from po_pos import po_pos_set
    po_pos_set(user_id, m)
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
    mc_flush_other(po.user_id, po.cid)

def po_cid_set(po, cid):
    o_cid = po.cid
    if cid != o_cid:
        po.cid = cid
        po.save()
        mc_flush_cid_list_all(po.user_id, [o_cid, cid])

def po_rm(user_id, id):
    po = Po.mc_get(id)
    if po.can_admin(user_id):
        from po_question import answer_count
        if po.cid == CID_QUESTION:
            if answer_count(id):
                return
        return _po_rm(user_id, po)

def _po_rm(user_id, po):
    po.state = STATE_DEL
    po.save()
    id = po.id
    feed_rm(id)
    from zsite_tag import zsite_tag_rm_by_po_id
    zsite_tag_rm_by_po_id(id)
    from rank import rank_rm_all
    rank_rm_all(id)
    from po_question import mc_answer_id_get, answer_count
    rid = po.rid
    if rid:
        mc_answer_id_get.delete('%s_%s' % (user_id, rid))
        answer_count.delete(rid)
    mc_flush(user_id, po.cid)
    return True

def po_word_new(user_id, name, state=STATE_ACTIVE, rid=0):
    if name and not is_same_post(user_id, name):
        m = po_new(CID_WORD, user_id, name, state, rid)
        if state > STATE_SECRET:
            m.feed_new()
        return m

def po_note_new(user_id, name, txt, state=STATE_ACTIVE):
    if not name and not txt:
        return
    name = name or time_title()
    if not is_same_post(user_id, name, txt):
        m = po_new(CID_NOTE, user_id, name, state)
        txt_new(m.id, txt)
        if state > STATE_SECRET:
            m.feed_new()
        return m


PO_LIST_STATE = {
    True: 'state>%s' % STATE_DEL,
    False: 'state>%s' % STATE_SECRET,
}


def _po_list_count(user_id, cid, is_self):
    qs = Po.where(user_id=user_id)
    if cid:
        qs = qs.where(cid=cid)
    return qs.where(PO_LIST_STATE[is_self]).count()

po_list_count = McNum(_po_list_count, 'PoListCount.%s')

mc_po_id_list = McLimitA('PoIdList.%s', 512)

@mc_po_id_list('{user_id}_{cid}_{is_self}')
def po_id_list(user_id, cid, is_self, limit, offset):
    qs = Po.where(user_id=user_id)
    if cid:
        qs = qs.where(cid=cid)
    return qs.where(PO_LIST_STATE[is_self]).order_by('id desc').col_list(limit, offset)

def po_view_list(user_id, cid, is_self, limit, offset=0):
    id_list = po_id_list(user_id, cid, is_self, limit, offset)
    return Po.mc_get_list(id_list)

def mc_flush_all(user_id):
    for is_self in (True, False):
        for cid in CID_PO:
            mc_flush_cid(user_id, cid, is_self)
        mc_flush_cid(user_id, 0, is_self)

def mc_flush(user_id, cid):
    mc_flush_cid_list_all(user_id, [0, cid])
    mc_feed_po_iter.delete(user_id)

def mc_flush_other(user_id, cid):
    mc_flush_cid(user_id, 0, False)
    mc_flush_cid(user_id, cid, False)
    mc_feed_po_iter.delete(user_id)

def mc_flush_cid(user_id, cid, is_self):
    key = '%s_%s_%s' % (user_id, cid, is_self)
    po_list_count.delete(key)
    mc_po_id_list.delete(key)

def mc_flush_cid_list_all(user_id, cid_list):
    for is_self in (True, False):
        for cid in cid_list:
            mc_flush_cid(user_id, cid, is_self)

if __name__ == '__main__':
    pass
