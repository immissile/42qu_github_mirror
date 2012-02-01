#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
CREATE TABLE  `zpage`.`import_feed` (
  `id` int(11) NOT NULL auto_increment,
  `title` varbinary(256) NOT NULL, `txt` blob NOT NULL,
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
from douban import DoubanUser, douban_feed_to_review_iter
from zkit.htm2txt import htm2txt
from zkit.txt import format_txt
from zkit.txt_img_fetch import txt_img_fetch
from kv import Kv
from duplicate import txt_is_duplicate, set_record

import_record = Kv('import_record',0)

class ImportFeed(Model):
    pass

IMPORT_FEED_STATE_INIT = 0
IMPORT_FEED_STATE_RM = 1
IMPORT_FEED_STATE_REVIEWED = 2
IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR = 3
IMPORT_FEED_STATE_PO_IS_CREATED = 4 #is needed?

def feed_next():
    return ImportFeed.where(state=IMPORT_FEED_STATE_INIT)[1]

def import_feed_rm(id):
    feed_state_set(id,IMPORT_FEED_STATE_RM)

def import_feed_new(title, txt, author_id, url, src_id, state=IMPORT_FEED_STATE_INIT):
    txt = format_txt(htm2txt(txt))
    if not txt_is_duplicate(txt):
        new_feed = ImportFeed(title=title, txt=txt, author_id=author_id, url=url, state=state , src_id = src_id)
        new_feed.save()
        set_record(new_feed.id)
        return new_feed

def feed_state_set(id, state):
    feed = ImportFeed.get(id)
    if feed:
        feed.state = state
        feed.save()

def zsite_id_by_douban_user_id(douban_user):
    zsite_id = 10001518
    if douban_user:
        douban_username = douban_user.name
        #TODO: get zsite_user_id
        zsite_id = 10001518
    return zsite_id


def feed2po(id, erase_author=False):
    feed = ImportFeed.get(id)
    if feed:
        if erase_author:
            zsite_id = 0
            user_id = 0
            po_rid = 0
            feed.state = IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR
        else:
            douban_user = DoubanUser.get(feed.author_id)
            user_id = zsite_id_by_douban_user_id(douban_user)
            if user_id == 0:
                zsite_id = feed.zsite_id
                po_rid = feed.author_id
            else:
                zsite_id = 0
            feed.state = IMPORT_FEED_STATE_REVIEWED

        feed.save()
        txt = txt_img_fetch(feed.txt)
        po = po_note_new(user_id, feed.title, txt, zsite_id = zsite_id)
        if po:
            import_record.set(po.id, feed.src_id)
            return po

def import_feed_by_douban_feed():
    for i in douban_feed_to_review_iter():
        import_feed_new(
            i.title, i.htm, i.user_id, i.cid, i.id
        )

if __name__ == '__main__':
    pass
    import_feed_by_douban_feed()
    #print ImportFeed.where(state = IMPORT_FEED_STATE_INIT)

