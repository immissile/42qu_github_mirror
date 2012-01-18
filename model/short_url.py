#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import  McModel
from config import SHORT_DOMAIN
from zkit.base58 import b58decode, b58encode
from txt2htm import RE_LINK_TARGET

class UrlShort(McModel):
    pass

def replace_link(match):
    gs = match.groups()
    b, g , e = gs
    if not (g.startswith('http://v.youku.com/v_show/id_') or g.startswith('http://player.youku.com/player.php/sid/')
            or g.endswith('.swf') or g.endswith('.jpg') or g.endswith('.png') or g.endswith('.gif') or g.startswith('http://%s'%SHORT_DOMAIN)):
        g = url_short(g)
    return g


def url_short(url):
    short_url = UrlShort.get(value=url)
    if not short_url:
        short_url = UrlShort(value=url)
        short_url.save()

    s_url_id = b58encode(short_url.id)

    link = 'http://%s/%s' % (SHORT_DOMAIN, s_url_id)
    return link

def url_short_by_id(id):
    id = b58decode(id)
    url = UrlShort.mc_get(id)
    if url:
        return url.value
    return None

def url_short_txt(s):
    if type(s) is unicode:
        s = str(s)
    s = '\r'.join(map(str.rstrip, s.replace('\r\n', '\r').replace('\n', '\r').split('\r')))
    s = RE_LINK_TARGET.sub(replace_link, s)
    return s

if __name__ == '__main__':
#for i in range(199):
#    print url_short("http://google"+str(i))

#print url_short_by_id('3T')
    print url_short_txt('sfsdfsdf http://google.com https://mail.google.com/mail/u/0/#inbox/134ec4da6de5b5a7 https://mail.google.com/mail/u/0/#inbox')
    print url_short_by_id('4x')
