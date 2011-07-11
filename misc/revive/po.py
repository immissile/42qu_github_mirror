#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.note import Note, NoteSubject, note_subject_id_by_man_id_note_id, note_subject_note_id_id_state
from model.po import po_new, po_note_new, po_word_new
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from model.zsite_tag import zsite_tag_new_by_tag_name
from model.zsite import Zsite


SITE_RT = (
    ('产品', 12609),
    ('产品', 14157),
    ('产品', 152),
    ('产品', 7319),
    ('产品', 783),
    ('产品', 7952),
    ('产品', 7983),
    ('传奇', 631),
    ('公司', 10884),
    ('公司', 12676),
    ('创业', 201),
    ('创业', 37),
    ('创业', 609),
    ('创业', 624),
    ('思考', 10345),
    ('思考', 10533),
    ('思考', 13616),
    ('思考', 784),
    ('思考', 799),
    ('思考', 8080),
    ('思考', 868),
    ('思考', 9331),
    ('思考', 959),
    ('技术', 10705),
    ('招聘', 11291),
    ('招聘', 910),
    ('招聘', 945),
    ('传奇', 11409),
    ('随笔', 113),
    ('随笔', 12371),
    ('随笔', 13434),
    ('随笔', 14682),
    ('随笔', 696),
    ('随笔', 7713),
    ('随笔', 7823),
)

from model.god_po_show import po_show_zsite_channel
PO_SHOW = dict((v, k) for k, v in po_show_zsite_channel())

PO_SHOW_DIC = dict((v, PO_SHOW[k]) for k, v in SITE_RT)

from model.po_show import po_show_set

import re
PIC_SUB = re.compile(r'<图片([\d]+)>')
def pic2pic(match):
    m = int(match.groups()[0])
    return ' 图:%s ' % m

from qu.mysite.util.pic import picopen
from qu.mysite.model.kvfs import fs_set_jpg, fs_url, fs_get
from model.po_pic import po_pic_new

def init_po():
    for i in Note.where():
        id = i.id
        user_id = i.man_id
        subject_id = note_subject_id_by_man_id_note_id(user_id, id)
        id, state = note_subject_note_id_id_state(subject_id, id)
        subject = NoteSubject.get(subject_id)
        if id and state:
            m = None
            if i.txt:
                title = i.title
                txt = PIC_SUB.sub(pic2pic, i.txt)
                print title, txt
                m = po_note_new(user_id, title, txt)
                if m:
                    name = subject.name
                    zsite_tag_new_by_tag_name(m, name)
                    for pic in i.pic_edit_list:
                        img = picopen(fs_get('note/0', '%s.jpg' % pic.id))
                        if img:
                            po_pic_new(user_id, m.id, img, pic.order)
                    if id in PO_SHOW_DIC:
                        po_show_set(m, PO_SHOW_DIC[id])
            else:
                m = po_word_new(user_id, i.title)
            if m:
                for r in i.reply_list():
                    from_user = Zsite.get(r.man_id)
                    m.reply_new(from_user, r.txt, r.state)


if __name__ == '__main__':
    init_po()
