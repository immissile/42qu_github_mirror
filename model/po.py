#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache, McNum
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_VIDEO, CID_AUDIO, CID_EVENT, CID_EVENT_FEEDBACK, CID_PO, CID_EVENT_NOTICE
from feed import feed_new, mc_feed_tuple, feed_rm
from feed_po import mc_feed_po_iter, mc_feed_po_dict
from gid import gid
from spammer import is_same_post
from state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from txt import txt_new, txt_get, txt_property
from zkit.time_format import time_title
from reply import ReplyMixin
from po_pic import pic_htm
from txt2htm import txt_withlink
from zsite import Zsite
from zkit.txt import cnencut
from zkit.attrcache import attrcache
from cgi import escape
#from sync import mq_sync_po_by_zsite_id

PO_CN_EN = (
    (CID_WORD, 'word', '微博', '句'),
    (CID_NOTE, 'note', '文章', '篇'),
    (CID_QUESTION, 'question', '问题', '条'),
    (CID_ANSWER, 'answer', '回答', '个'),
    (CID_PHOTO, 'photo', '图片', '张'),
    (CID_VIDEO, 'video', '视频', '场'),
    (CID_AUDIO, 'audio', '声音', '段'),
    (CID_EVENT, 'event', '活动', '次'),
)
PO_SHARE_FAV_CID = set([i[0] for i in PO_CN_EN])
PO_EN = dict((i[0], i[1]) for i in PO_CN_EN)
PO_CN = dict((i[0], i[2]) for i in PO_CN_EN)
PO_COUNT_CN = dict((i[0], i[3]+i[2]) for i in PO_CN_EN)

mc_htm = McCache('PoHtm.%s')

class Po(McModel, ReplyMixin):

    @property
    def txt(self):
        cid = self.cid
        if cid in (CID_WORD, CID_EVENT_NOTICE):
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
            user_id = self.user_id
            s = pic_htm(s, user_id, id)
        return s

    def txt_set(self, txt):
        id = self.id
        txt_new(id, txt or '')
        self.mc_flush()

    @attrcache
    def user(self):
        return Zsite.mc_get(self.user_id)

    @attrcache
    def target(self):
        if self.cid in (CID_WORD, CID_ANSWER, CID_EVENT_NOTICE, CID_EVENT_FEEDBACK):
            return Po.mc_get(self.rid)

    question = target

    @attrcache
    def name(self):
        cid = self.cid
        q = self.target
        if q:
            if cid == CID_EVENT_FEEDBACK:
                if q.user_id == self.user_id:
                    name = '总结 : %s'
                else:
                    name = '评价 : %s'
                return name % q.name

            if cid != CID_EVENT_NOTICE:
                return '答 : %s' % q.name

        return self.name_

    @attrcache
    def name_with_user(self):
        q = self.target
        if q:
            u = self.user
            return '%s 答 : %s' % (u.name, q.name)
        return self.name_

    @attrcache
    def name_htm(self):
        q = self.target
        cid = self.cid

        if cid == CID_EVENT_NOTICE:
            return txt_withlink(self.name_)

        if q:
            u = q.user
            link = '<a href="%s">%s</a>' % (q.link, escape(q.name))

            if cid == CID_EVENT_FEEDBACK:
                if q.user_id == self.user_id:
                    name = '总结 : %s'
                else:
                    name = '评价 : %s'
                return name%link
            else:
                if q.user_id == self.user_id:
                    return '自问自答 : %s' % link
                else:
                    return '答 <a href="%s">%s</a> 问 : %s' % (
                        u.link, escape(u.name), link
                    )

        if cid == CID_WORD:
            return txt_withlink(self.name)

        return escape(self.name)

    @attrcache
    def link(self):
        u = self.user
        #TODO REMOVE
        if u:
            return '%s/%s' % (u.link, self.id)

    @attrcache
    def link_target(self):
        q = self.target
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
        if user_id:
            return self.user_id == user_id

    def reply_new(self, user, txt, state=STATE_ACTIVE):
        result = super(Po, self).reply_new(user, txt, state)
        mc_feed_tuple.delete(self.id)
        return result

    def tag_new(self):
        from zsite_tag import zsite_tag_new_by_tag_id, tag_id_by_user_id_cid
        cid = self.cid
        state = self.state
        user_id = self.user_id
        if cid not in (CID_WORD, CID_EVENT, CID_EVENT_FEEDBACK, CID_EVENT_NOTICE) and state == STATE_ACTIVE:
            tag_id = tag_id_by_user_id_cid(user_id, cid)
            zsite_tag_new_by_tag_id(self, tag_id)

    def tag_rm(self):
        from zsite_tag import zsite_tag_rm_by_po
        zsite_tag_rm_by_po(self)


def po_new(cid, user_id, name, state, rid=0, id=None):
    m = Po(
        id=id or gid(),
        name_=cnencut(name, 142),
        user_id=user_id,
        cid=cid,
        rid=rid,
        state=state,
        create_time=int(time()),
    )
    m.save()
    #if cid in (CID_NOTE, CID_WORD) and state == STATE_ACTIVE:
        #mq_sync_po_by_zsite_id(user_id, m.id)
    from po_pos import po_pos_set
    po_pos_set(user_id, m)
    mc_flush(user_id, cid)
    m.tag_new()
    return m

def po_state_set(po, state):
    from buzz import mq_buzz_po_rm
    old_state = po.state
    if old_state == state:
        return
    po.state = state
    po.save()
    mc_flush_other(po.user_id, po.cid)

    if old_state > STATE_SECRET and state == STATE_SECRET:
        feed_rm(id)
        po.tag_rm()
        mq_buzz_po_rm(id)
        from fav import fav_rm_by_po
        fav_rm_by_po(po)
    elif old_state <= STATE_SECRET and state >= STATE_ACTIVE:
        po.feed_new()
        po.tag_new()

def po_cid_set(po, cid):
    o_cid = po.cid
    if cid != o_cid:
        po.cid = cid
        po.save()
        mc_flush_cid_list_all(po.user_id, [o_cid, cid])

def po_rm(user_id, id):
    po = Po.mc_get(id)
    cid = po.cid
    rid = po.rid
    if po.can_admin(user_id):
        from po_question import answer_count

        if cid == CID_QUESTION:
            if answer_count(id):
                return
        elif cid == CID_EVENT:
            from model.event import event_rm
            event_rm(user_id, id)
        elif cid == CID_EVENT_FEEDBACK:
            from model.po_event import po_event_feedback_rm
            from model.rank import rank_rm
            po_event_feedback_rm(user_id, rid)
            rank_rm(id, rid)
        elif cid == CID_EVENT_NOTICE:
            from model.po_event import mc_po_event_notice_id_list_by_event_id
            mc_po_event_notice_id_list_by_event_id.delete(rid)

        return _po_rm(user_id, po)


def _po_rm(user_id, po):
    po.state = STATE_DEL
    po.save()
    id = po.id
    feed_rm(id)
    from zsite_tag import zsite_tag_rm_by_po
    zsite_tag_rm_by_po(po)
    from rank import rank_rm_all
    rank_rm_all(id)
    from po_question import mc_answer_id_get, answer_count
    rid = po.rid
    if rid:
        mc_answer_id_get.delete('%s_%s' % (user_id, rid))
        answer_count.delete(rid)
    mc_flush(user_id, po.cid)
    from buzz import mq_buzz_po_rm
    mq_buzz_po_rm(id)
    from fav import fav_rm_by_po
    fav_rm_by_po(po)
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
    po = Po.mc_get(10066676)
    #print po.name
