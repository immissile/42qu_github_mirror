#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import Model
from po import po_note_new
from douban import DoubanUser
from zkit.htm2txt import htm2txt
from zkit.txt import format_txt
from zkit.txt_img_fetch import txt_img_fetch
from 

class ImportFeed(Model):
    pass

STATE_INIT = 0
STATE_DISALLOWED = 1
STATE_ALLOWED = 2
STATE_ALLOWED_WITHNO_AUTHOR = 3
STATE_PO_IS_CREATED = 4 #is needed?

def new_import_feed(title, body, author_id, url, state=STATE_INIT):
    new_feed = ImportFeed(title=title, body=body, author_id=author_id, url=url, state=state)
    new_feed.save()
    return new_feed

def set_feed_state(id, state):
    feed = ImportFeed.get(id)
    if feed:
        feed.state = state

def get_zsite_user_id(douban_user):
    zsite_id = 0
    if douban_user:
        douban_username = douban_user.name
        #TODO: get zsite_user_id
        zsite_id = 10000000
    return zsite_id

def get_feed_domain_zsite_id(url):
    #TODO: fill code
    zsite_id = 1
    return zsite_id

def allow_feed(id, erase_author=False):
    feed = ImportFeed.get(id)
    if feed:
        if erase_author:
            user_id = 0
            po_rid = 0
            zsite_id = 0
        else:
            douban_user = DoubanUser.get(feed.author_id)
            user_id = get_zsite_user_id(douban_user)
            if user_id == 0:
                zsite_id = get_feed_domain_zsite_id(feed.url)
                po_rid = feed.author_id
        body = format_txt(htm2txt(feed.body))
        body = txt_img_fetch(body)
        po_note_new(user_id, feed.title, body, zsite_id = zsite_id)



