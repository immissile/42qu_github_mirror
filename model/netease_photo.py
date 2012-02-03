#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, mc
from zkit.htm2txt import htm2txt, unescape

class NeteaseUser(McModel):
    pass
class NeteasePhoto(McModel):
    pass
class NeteaseAlbum(McModel):
    pass

def netease_user_new(id, url, nickname, name):
    o = NeteaseUser.get(id)
    if not o:
        o = NeteaseUser(id=id, url=url, nickname=nickname, name=name).save()
    return o.id

def netease_photo_new(url, album_id):
    o = NeteasePhoto.get(url=url)
    if not o:
        o = NeteasePhoto(url=url, album_id=album_id).save()
    return o.id

def netease_album_new(id, title, user_id, place, published, url):
    o = NeteaseAlbum.get(id)
    if not o:
        o = NeteaseAlbum(id=id,title=title,user_id=user_id,place=place,published=published,url=url).save()
    return o.id

if __name__ == '__main__':
    print NeteasePhoto.count()
    print NeteaseAlbum.count()
    print NeteaseUser.count()
