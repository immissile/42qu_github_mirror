#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum, McCacheM
from cid import CID_VIDEO
from model.po import po_new , txt_new , is_same_post , STATE_SECRET, STATE_ACTIVE, time_title

VIDEO_CID_YOUKU = 1


HTM_YOUKU = '''<embed src="http://static.youku.com/v/swf/qplayer.swf?VideoIDS=%s=&isShowRelatedVideo=false&showAd=0&winType=interior" quality="high" class="video" allowfullscreen="true" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" wmode= "Opaque"></embed>'''
HTM_AUTOPLAY_YOUKU = '''<embed src="http://static.youku.com/v/swf/qplayer.swf?VideoIDS=%s=&isShowRelatedVideo=false&showAd=0&winType=interior&isAutoPlay=true" quality="high" class="video" allowfullscreen="true" align="middle" allowScriptAccess="sameDomain" type="application/x-shockwave-flash" wmode= "Opaque"></embed>'''

VIDEO_CID2HTM = {
    VIDEO_CID_YOUKU:HTM_YOUKU
}
VIDEO_CID2HTM_AUTOPLAY = {
    VIDEO_CID_YOUKU:HTM_AUTOPLAY_YOUKU
}


mc_video_uri = McCache('VideoUri:%s')

class Video(Model):
    pass


def video_htm_autoplay(cid, id):
    return VIDEO_CID2HTM_AUTOPLAY[cid] % video_uri(id)

def video_htm(cid, id):
    return VIDEO_CID2HTM[cid] % video_uri(id)


@mc_video_uri('{id}')
def video_uri(id):
    c = Video.raw_sql('select uri from video where id=%s', id)
    r = c.fetchone()
    if r:
        return r[0]
    return ''

def video_new(id, uri):
    v = Video.get_or_create(id=id)
    v.uri = uri
    v.save()
    mc_video_uri.set(id, uri)

def po_video_new(user_id, name, txt, uri, state):

    if not name and not txt:
        return

    name = name or time_title()

    if not is_same_post(user_id, name, txt, uri):
        m = po_new(CID_VIDEO, user_id, name, state, VIDEO_CID_YOUKU)
        video_new(m.id , uri)
        m.txt_set(txt)
        m.feed_new()
        return m


if __name__ == '__main__':
    pass
