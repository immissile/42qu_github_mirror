#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.note import Note, NoteSubject
from model.po import po_new, po_note_new, po_word_new, note_subject_id_by_man_id_note_id, note_subject_note_id_id_state
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
    ('故事', 11409),
    ('随笔', 113),
    ('随笔', 12371),
    ('随笔', 13434),
    ('随笔', 14682),
    ('随笔', 696),
    ('随笔', 7713),
    ('随笔', 7823),
)


def init_po():
    for i in Note.where():
        id = i.id
        user_id = i.man_id
        subject_id = note_subject_id_by_man_id_note_id(id)
        id, state = note_subject_note_id_id_state(subject_id, id)
        subject = NoteSubject.get(subject_id)
        if id and state:
            if i.txt:
                m = po_note_new(user_id, i.title, i.txt)
                name = subject.name
                zsite_tag_new_by_tag_name(m, name)
            else:
                m = po_word_new(user_id, i.title)
