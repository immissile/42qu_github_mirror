#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.mysite.model.note import Note
from model.po import po_new, po_note_new, po_word_new
from model.state import STATE_DEL, STATE_SECRET, STATE_ACTIVE
from model.zsite_tag import zsite_tag_new_by_tag_name
from model.zsite import Zsite

def init_po():
    for i in Note.where():
        user_id = i.man_id
        subject = 
