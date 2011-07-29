#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum, McCacheM
from cid import CID_VIDEO
from model.po import po_new , txt_new , is_same_post , STATE_SECRET, STATE_ACTIVE, time_title
from zsite_tag import ZsiteTagPo, zsite_tag_new_by_tag_id

VEDIO_CID_YOUKU = 1

class Video(Model):
    pass

def video_new(id, uri):
    v = Video.get_or_create(id=id)
    v.uri = uri
    v.save()

def po_video_new(user_id, name, txt, uri, state):

    if not name and not txt:
        return

    name = name or time_title()

    if not is_same_post(user_id, name, txt, uri):
        m = po_new(CID_VIDEO, user_id, name, state, VEDIO_CID_YOUKU)
        video_new(m.id , uri)
        m.txt_set(txt)
        m.feed_new()

        zsite_tag_new_by_tag_id(m, 1)

        return m


if __name__ == '__main__':
    pass
