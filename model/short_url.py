#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import  Model
from config import SHORT_DOMAIN
from zkit.base58 import b58decode, b58encode
from zkit.img_filter import img_filter
from txt2htm import RE_LINK_TARGET

class UrlShort(Model):
    pass

def replace_link(match, user_id):
    from po_video import  video_filter
    gs = match.groups()
    b, g , e = gs
    if not ( video_filter(g)[0] or img_filter(g) or g.startswith('http://%s'%SHORT_DOMAIN)):
        g = url_short(g, user_id)
    return g


def url_short(url, user_id=0):
    short_url = UrlShort(value=url, user_id=user_id)
    short_url.save()
    s_url_id = b58encode(short_url.id)

    link = 'http://%s/%s' % (SHORT_DOMAIN, s_url_id)
    return link

def url_short_by_id(id):
    print id
    id = b58decode(id)
    url = UrlShort.get(id)
    if url:
        return url.value
    return None

url_short_txt(s, user_id=0):
    if type(s) is unicode:
        s = str(s)
    s = RE_LINK_TARGET.sub(lambda match:replace_link(match,user_id), s)
    return s

if __name__ == '__main__':
#for i in range(199):
#    print url_short("http://google"+str(i))

#print url_short_by_id('3T')
    print url_short_txt('sfsdfsdf http://g.cn/df.png http://google.com https://mail.google.com/mail/u/0/#inbox/134ec4da6de5b5a7 https://mail.google.com/mail/u/0/#inbox')
    print url_short_by_id('4x')
