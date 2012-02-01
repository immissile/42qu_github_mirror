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


CREATE TABLE `zpage`.`import_po_user` (
  `id` int  NOT NULL,
  `name` varchar(128)  NOT NULL,
  `cid` SMALLINT  NOT NULL,
  `url` int  NOT NULL,
  PRIMARY KEY (`id`)
)
ENGINE = MyISAM;

'''

import _env
from _db import Model
from po import po_note_new
from douban import DoubanUser, douban_feed_to_review_iter, user_id_by_feed_id
from zkit.htm2txt import htm2txt
from zkit.txt import format_txt
from zkit.txt_img_fetch import txt_img_fetch
from kv import Kv
from duplicate import Duplicator
from url_short import url_short2id
from site_sync import site_sync_new


douban_duplicator = Duplicator('douban_duplicator.kch')

class ImportRecord(Model):
    pass

class ImportFeed(Model):
    pass

IMPORT_FEED_STATE_INIT = 0
IMPORT_FEED_STATE_RM = 1

IMPORT_FEED_STATE_REVIEWED = 2
IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR = 3
IMPORT_FEED_STATE_REVIEWED_SYNC = 4
IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC = 5

IMPORT_FEED_STATE_PO_IS_CREATED = 6 #is needed?

DOUBAN_ZSITE_ID = 68615

def feed_next():
    return ImportFeed.where(state=IMPORT_FEED_STATE_INIT)[1]

def import_feed_rm(id):
    feed_state_set(id,IMPORT_FEED_STATE_RM)

def import_feed_new(title, txt, author_id, url, src_id, zsite_id, state=IMPORT_FEED_STATE_INIT):
    txt = format_txt(htm2txt(txt))
    if not douban_duplicator.txt_is_duplicate(txt):

        douban_user = DoubanUser.get(author_id)
        user_id = zsite_id_by_douban_user_id(douban_user)

        new_feed = ImportFeed(
                title=title, 
                txt=txt, 
                user_id=user_id, 
                zsite_id=zsite_id,
                state=state, 
                rid = src_id, 
                url=url
                )

        new_feed.save()
        douban_duplicator.set_record(txt, new_feed.id)

        return new_feed

def feed_state_set(id, state):
    feed = ImportFeed.get(id)
    if feed:
        feed.state = state
        feed.save()

def zsite_id_by_douban_user_id(douban_user):
    zsite_id = 0
    if douban_user:
        douban_username = douban_user.name
        #TODO: get zsite_user_id
        zsite_id = 10001518
    return zsite_id

def feed2po_new():
    from zweb.orm import ormiter
    for feed in ormiter(ImportFeed,'state=%s or state=%s or state=%s or state=%s'%(
                IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR, 
                IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC,
                IMPORT_FEED_STATE_REVIEWED,
                IMPORT_FEED_STATE_REVIEWED_SYNC)
                ):
        txt = txt_img_fetch(feed.txt)

        user_id = feed.user_id
        zsite_id = feed.zsite_id

        if feed.state==IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC or feed.state == IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR:
                user_id = 0
                zsite_id = 0

        po = po_note_new(user_id, feed.title, txt, zsite_id = zsite_id)

        if po:

            record = ImportRecord.get_or_create(id = po.id)
            record.user_id = user_id_by_feed_id(feed.rid)
            record.url_id = url_short2id(feed.url)
            record.save()

            if feed.state>=IMPORT_FEED_STATE_REVIEWED_SYNC:
                #site_sync_new(po.id)
                pass
            
            feed.state = IMPORT_FEED_STATE_PO_IS_CREATED
            feed.save()

def review_feed(id, erase_author=False, sync=False):
    feed = ImportFeed.get(id)
    if feed:
        if erase_author:
            if sync:
                feed.state = IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC
            else:
                feed.state = IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR
        else:
            if sync:
                feed.state = IMPORT_FEED_STATE_REVIEWED_SYNC
            else:
                feed.state = IMPORT_FEED_STATE_REVIEWED

        feed.save()

def import_feed_by_douban_feed():
    for i in douban_feed_to_review_iter():
        import_feed_new(
            i.title, i.htm, i.user_id, i.link, i.id, DOUBAN_ZSITE_ID
        )

if __name__ == '__main__':
    pass
    #import_feed_by_douban_feed()
    #print ImportFeed.where(state = IMPORT_FEED_STATE_INIT)
    feed2po_new()

