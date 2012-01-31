#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import  Model
from config import SHORT_DOMAIN
from zkit.num2code import num_decode, num_encode
from zkit.img_filter import img_filter
from txt2htm import RE_LINK_TARGET


SHORT_LINK = 'http://%s'%SHORT_DOMAIN
class UrlShort(Model):
    pass

def replace_link(match, user_id):
    from po_video import  video_filter
    gs = match.groups()
    b, g , e = gs
    if not ( video_filter(g)[0] or img_filter(g) or g.startswith(SHORT_LINK) ):
        g = url_short(g, user_id)
    return g


def url_short(url, user_id=0):
    url = url.strip()
    if url:
        url_short = UrlShort.get_or_create(value=url, user_id=user_id)
        url_short.save()
        s_url_id = num_encode(url_short.id)

        link = '%s/%s' % (SHORT_LINK, s_url_id)
        return link
    return ""

def url_short_by_key(key):
    id = num_decode(key)
    return url_short_by_id(id)

def url_short_by_id(id):
    url = UrlShort.get(id)
    if url:
        return url.value
    return ""

def url_short_txt(s, user_id=0):
    #TODO remove
    return s

    if type(s) is unicode:
        s = str(s)
    s = RE_LINK_TARGET.sub(lambda match:replace_link(match,user_id), s)
    return s

if __name__ == '__main__':
#for i in range(199):
#    print url_short("http://google"+str(i))

#print url_short_by_id('3T')
    #print url_short_txt('sfsdfsdf http://g.cn/df.png http://google.com https://mail.google.com/mail/u/0/#inbox/134ec4da6de5b5a7 https://mail.google.com/mail/u/0/#inbox')
    print url_short("http://baidu.com")
