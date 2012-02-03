#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import Model, McModel
from po import po_note_new
from douban import DoubanUser, douban_feed_to_review_iter, douban_user_by_feed_id , title_normal
from model.txt_img_fetch import txt_img_fetch
from kv import Kv
from url_short import url_short_id
from site_sync import site_sync_new
from rec_read import rec_cid_push
from po_by_tag import zsite_tag_po_new_by_name, tag_po_rm_by_po_id
from part_time_job import part_time_job_new
from config import PART_TIME_CID_IMPORT_FEED


IMPORT_FEED_STATE_RM = 0
IMPORT_FEED_STATE_INIT = 10

IMPORT_FEED_STATE_REVIEWED = 20
IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR = 30
IMPORT_FEED_STATE_REVIEWED_SYNC = 40
IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC = 50

IMPORT_FEED_STATE_POED = 60 

DOUBAN_ZSITE_ID = 10216239

IMPORT_FEED_CID_DICT = {
        DOUBAN_ZSITE_ID : 1, #douban
        }

class PoMeta(McModel):
    pass

class ImportFeed(Model):
    pass

class PoMetaUser(McModel):
    @property
    def link(self):
        if self.cid == DOUBAN_ZSITE_ID:
            return 'http://www.douban.com/people/%s'%self.url

def user_url_by_po_meta_user_id(id):
    user = PoMetaUser.mc_get(id)
    if user:
        if user.cid == DOUBAN_ZSITE_ID:
            return 'http://www.douban.com/people/%s'%user_id.url

def user_by_feed_id_zsite_id(feed_id, zsite_id):
    if zsite_id == DOUBAN_ZSITE_ID:
        return douban_user_by_feed_id(feed_id)

def feed_next():
    return ImportFeed.where(state=IMPORT_FEED_STATE_INIT)[1]

def import_feed_rm(id, current_user_id):
    part_time_job_new(PART_TIME_CID_IMPORT_FEED, id, current_user_id)
    feed_state_set(id, IMPORT_FEED_STATE_RM)


def feed_state_set(id, state):
    feed = ImportFeed.get(id)
    if feed:
        feed.state = state
        feed.save()

def zsite_id_by_douban_user_id(douban_user):
    #TODO: get zsite_user_id
    return 0
    zsite_id = 0
    if douban_user:
        douban_username = douban_user.name
        zsite_id = 10001518
    return zsite_id

def feed2po_new():
    from zweb.orm import ormiter
    for feed in ormiter(
            ImportFeed,
            'state>%s and state<%s'%(
                IMPORT_FEED_STATE_INIT,
                IMPORT_FEED_STATE_POED
            )
        ):
        txt = txt_img_fetch(feed.txt)
        feed_user = user_by_feed_id_zsite_id(feed.rid, feed.zsite_id)
        user_id = zsite_id_by_douban_user_id(feed_user)

        zsite_id = feed.zsite_id

        is_without_author = ((feed.state == IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC) or (feed.state == IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR))

        if is_without_author:
            user_id = 0
            zsite_id = 0

        title = title_normal(feed.title)
        po = po_note_new(user_id, title, txt, zsite_id=zsite_id)

        if po:
            if not feed_user:
                feed_user_id = 0
            else:
                user = PoMetaUser.get_or_create(name = feed_user.name, cid = zsite_id)
                user.url = feed_user.id

                user.save()

                feed_user_id = user.id

            record = PoMeta.get_or_create(id = po.id)
            record.user_id = feed_user_id
            record.url_id = url_short_id(feed.url)

            record.save()

            if not is_without_author:
                po.rid = record.id
                po.save()

            if feed.state >= IMPORT_FEED_STATE_REVIEWED_SYNC:
                site_sync_new(po.id)

            feed.state = IMPORT_FEED_STATE_POED
            feed.save()

            rec_cid_push(feed.cid, po.id)
            po_tag_new(feed.tags, po)

def review_feed(id, cid, title, txt, tags, current_user_id, author_rm=False, sync=False):
    feed = ImportFeed.get(id)
    if feed and feed.state==IMPORT_FEED_STATE_INIT :
        if author_rm:
            if sync:
                feed.state = IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC
            else:
                feed.state = IMPORT_FEED_STATE_REVIEWED_WITHOUT_AUTHOR
        else:
            if sync:
                feed.state = IMPORT_FEED_STATE_REVIEWED_SYNC
            else:
                feed.state = IMPORT_FEED_STATE_REVIEWED

        feed.title = title
        feed.txt = txt
        feed.cid = cid
        feed.tags = tags
        
        part_time_job_new(PART_TIME_CID_IMPORT_FEED, feed.id, current_user_id)

        feed.save()

def po_tag_new(tags, po):
    tag_po_rm_by_po_id(po.id)

    tags = tags.split(',')
    for tag in tags:
        zsite_tag_po_new_by_name(tag, po, 100)

if __name__ == '__main__':
    pass
    #import_feed_by_douban_feed()
    #print ImportFeed.where(state = IMPORT_FEED_STATE_INIT)
    #feed2po_new()
    from zweb.orm import ormiter
    for i in ormiter(ImportFeed):
        i.txt = i.txt.replace("豆友","网友").replace("豆油","私信").replace("豆邮","私信")
        i.save()

