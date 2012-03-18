#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McNum, McCacheM
from cgi import escape
from cid import CID_AUDIO
from model.po import po_new , txt_new , is_same_post , STATE_SECRET, STATE_ACTIVE, time_title
from fs import fs_set_audio
from config import FS_URL

HTM_AUDIO = '''<embed flashvars="foreColor=#aa1100&amp;analytics=false&amp;filename=%%s" quality="high" bgcolor="#FFFFFF" class="audio" src="%s/swf/1bit.swf" type="application/x-shockwave-flash" wmode= "Opaque"></embed>''' % FS_URL


def audio_save(id, audio):
    fs_set_audio('mp3', id, audio)


def po_audio_new(user_id, name, txt, audio, state, zsite_id):

    if not name and not txt:
        return

    name = name or time_title()

    m = po_new(
        CID_AUDIO,
        user_id, name, state, rid=0, zsite_id=zsite_id
    )
    if m:
        audio_save(m.id, audio)
        m.txt_set(txt)
        m.feed_new()
        return m


if __name__ == '__main__':
    pass
