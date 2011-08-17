#!/usr/bin/env python
# -*- coding: utf-8 -*-
from time import time
from _db import cursor_by_table, McModel, McLimitA, McCache, McNum
from cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_VIDEO, CID_AUDIO, CID_EVENT, CID_EVENT_FEEDBACK, CID_PO
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

PO_CN_EN = (
    (CID_WORD, 'word', '微博', '句'),
    (CID_NOTE, 'note', '文章', '篇'),
    (CID_QUESTION, 'question', '问题', '条'),
    (CID_ANSWER, 'answer', '回答', '个'),
    (CID_PHOTO, 'photo', '图片', '张'),
    (CID_VIDEO, 'video', '视频', '场'),
    (CID_AUDIO, 'audio', '音乐', '段'),
    (CID_EVENT, 'event', '活动', '次'),
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
        cid = self.cid
        if q:

__name__ == '__main__':
    pass
