#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import McModel


class NeteaseUser(McModel):
    pass


class NeteasePhoto(McModel):
    pass


class NeteaseAlbum(McModel):
    pass


def netease_user_new(id, url, nickname, name):
    o = NeteaseUser.get_or_create(id=id)
    o.url = url
    o.nickname = nickname
    o.name = name
    o.save()
    return o.id


def netease_photo_new(url, album_id):
    o = NeteasePhoto.get_or_create(url=url)
    o.album_id = album_id
    o.save()
    return o.id


def netease_album_new(id, title, user_id, place, published, url):
    o = NeteaseAlbum.get_or_create(id=id)
    o.title = title
    o.user_id = user_id
    o.place = place
    o.published = published
    o.url = url
    o.save()
    return o.id

if __name__ == '__main__':
    print NeteasePhoto.count()
    print NeteaseAlbum.count()
    print NeteaseUser.count()
