#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.note import Note, NoteSubject
from model.po import po_new, po_note_new, po_word_new, note_subject_id_by_man_id_note_id, note_subject_note_id_id_state
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from model.zsite_tag import zsite_tag_new_by_tag_name
from model.zsite import Zsite

def init_po():
    for i in Note.where():
        id = i.id
        user_id = i.man_id
        subject_id = note_subject_id_by_man_id_note_id(id)
        id, state = note_subject_note_id_id_state(subject_id, id)
        subject = NoteSubject.get(subject_id)
        if id and state:
            name = subject.name
