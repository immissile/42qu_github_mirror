#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
CREATE TABLE  `zpage`.`import_feed` (
  `id` int(11) NOT NULL auto_increment,
  `title` varbinary(256) NOT NULL, `body` blob NOT NULL,
  `author_id` int(11) NOT NULL,
  `url` varbinary(1024) NOT NULL,
  `state` int(11) NOT NULL,
  `src_id` int(11) NOT NULL,
  PRIMARY KEY  (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=binary

CREATE TABLE `zpage`.`import_record` (
  `key` int  NOT NULL,
  `value` int  NOT NULL,
  PRIMARY KEY (`key`)
)
ENGINE = MyISAM;

'''


import _env
from _db import Model
from po import po_note_new
from douban import DoubanUser, get_most_rec_and_likes
from zkit.htm2txt import htm2txt
from zkit.txt import format_txt
from zkit.txt_img_fetch import txt_img_fetch
from kv import Kv
from duplicate import txt_is_duplicate, set_record

import_record = Kv('import_record',0)

class ImportFeed(Model):
    pass

STATE_INIT = 0
STATE_DISALLOWED = 1
STATE_ALLOWED = 2
STATE_ALLOWED_WITHNO_AUTHOR = 3
STATE_PO_IS_CREATED = 4 #is needed?

def get_feed_2_edit():
    feed = ImportFeed.where(state = STATE_INIT)
    if len(feed)>1:
        return feed[1]

def rm_import_feed(id):
    set_feed_state(id,STATE_DISALLOWED)

def new_import_feed(title, body, author_id, url, src_id, state=STATE_INIT):
    body = format_txt(htm2txt(body))
    if not txt_is_duplicate(body):
        new_feed = ImportFeed(title=title, body=body, author_id=author_id, url=url, state=state , src_id = src_id)
        new_feed.save()
        set_record(body,new_feed.id)
        return new_feed

def set_feed_state(id, state):
    feed = ImportFeed.get(id)
    if feed:
        feed.state = state
        feed.save()

def get_local_user_id(douban_user):
    zsite_id = 0
    if douban_user:
        douban_username = douban_user.name
        #TODO: get zsite_user_id
        zsite_id = 10001518
    return zsite_id

def get_feed_domain_zsite_id(url):
    #TODO: get Domain => zsite_id
    #TODO:Currently using 豆瓣的
    zsite_id = 68615 #@dev machine
    return zsite_id

def feed_2_po(id, erase_author=False):
    feed = ImportFeed.get(id)
    if feed:
        if erase_author:
            zsite_id = 0
            user_id = 0
            po_rid = 0
            feed.state = STATE_ALLOWED_WITHNO_AUTHOR

        else:
            douban_user = DoubanUser.get(feed.author_id)
            user_id = get_local_user_id(douban_user)
            if not user_id :
                zsite_id = get_feed_domain_zsite_id(feed.url)
                po_rid = feed.author_id
            else:
                zsite_id = 0
                po_rid = 0 
            feed.state = STATE_ALLOWED

        feed.save()
        body = txt_img_fetch(feed.body)
        po = po_note_new(user_id, feed.title, body, zsite_id = zsite_id)
        if po:
            po.rid = po_rid
            po.save()

            import_record.set(po.id, feed.src_id)
            return po

def fetch_feed():
    for i in get_most_rec_and_likes():
        new_import_feed(i.title, i.htm, i.user_id, i.cid, i.id)

if __name__ == '__main__':
    pass
    fetch_feed()
    #print ImportFeed.where(state = STATE_INIT)

