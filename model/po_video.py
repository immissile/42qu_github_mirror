#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from _db import Model, McModel, McCache, McCacheA, McNum, McCacheM
from cid import CID_VIDEO
from model.po import po_new , txt_new , is_same_post , STATE_SECRET, STATE_ACTIVE, time_title
from video_swf import video_filter, video_link_by_cid_uri, VIDEO_CID2LINK_AUTOPLAY, _HTM_SWF

mc_video_uri = McCache('VideoUri:%s')

class Video(Model):
    pass


@mc_video_uri('{id}')
def video_uri(id):
    c = Video.raw_sql('select uri from video where id=%s', id)
    r = c.fetchone()
    if r:
        return r[0]
    return ''

def video_link_autoplay(cid, id):
    return video_link_by_cid_uri(cid, video_uri(id), VIDEO_CID2LINK_AUTOPLAY)

def video_htm_autoplay(cid, id):
    return _HTM_SWF%video_link_autoplay(cid, id)

def video_htm(cid, id):
    return _HTM_SWF%video_link_by_cid_uri(cid, video_uri(id))

def video_new(id, uri):
    v = Video.get_or_create(id=id)
    v.uri = uri
    v.save()
    mc_video_uri.set(id, uri)


def po_video_new(user_id, name, txt, uri, video_site, state, zsite_id):

    if not name and not txt:
        return

    name = name or time_title()

    if not is_same_post(user_id, name, txt, uri):
        m = po_new(
            CID_VIDEO, user_id, name, state, video_site,
            zsite_id=zsite_id
        )
        if m:
            video_new(m.id , uri)
            m.txt_set(txt)
            m.feed_new()
            return m


if __name__ == '__main__':
    pass
    print
    s = 'http://static.slidesharecdn.com/swf/ssplayer2.swf?doc=bp2011-111130022417-phpapp02&'



