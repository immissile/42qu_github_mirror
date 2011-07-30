#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum, McCacheM
from cgi import escape
from cid import CID_AUDIO
from model.po import po_new , txt_new , is_same_post , STATE_SECRET, STATE_ACTIVE, time_title
from zsite_tag import ZsiteTagPo, zsite_tag_new_by_tag_id
from fs import fs_set_audio

def audio_save(id, audio):
    fs_set_audio('0', id, audio)


def po_audio_new(user_id, name, txt, audio):
    state = STATE_ACTIVE

    if not name and not txt:
        return

    name = name or time_title()
    if not is_same_post(user_id, name, txt):

        state = STATE_ACTIVE
        m = po_new(CID_AUDIO, user_id, name, state, rid=0)
        audio_save(m.id, audio)
        m.txt_set(txt)
        if state > STATE_SECRET:
            m.feed_new()

        zsite_tag_new_by_tag_id(m, 1)

        return m


if __name__ == '__main__':
    pass
