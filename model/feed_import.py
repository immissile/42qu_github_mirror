#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import Model, McModel, redis
from po import po_note_new
from kv import Kv
from rec_read import  rec_read_new, REDIS_REC_CID_DICT
from part_time_job import part_time_job_new
from config.privilege import PRIVILEGE_FEED_IMPORT
from zrank.sorts import hot


FEED_IMPORT_STATE_RM = 0
FEED_IMPORT_STATE_WITHOUT_TAG = 10
FEED_IMPORT_STATE_INIT = 20
FEED_IMPORT_STATE_REVIEWED = 30
FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR = 40
FEED_IMPORT_STATE_REVIEWED_SYNC = 50
FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC = 60
FEED_IMPORT_STATE_POED = 70 



class PoMeta(McModel):
    pass

class FeedImport(Model):
    pass

class PoMetaUser(McModel):
    @property
    def link(self):
        if self.cid == ZSITE_DOUBAN_ID:
            return 'http://www.douban.com/people/%s'%self.url

def user_url_by_po_meta_user_id(id):
    user = PoMetaUser.mc_get(id)
    if user:
        if user.cid == ZSITE_DOUBAN_ID:
            return 'http://www.douban.com/people/%s'%user_id.url


def feed_next():
    fdlist = FeedImport.where(state=FEED_IMPORT_STATE_INIT)[1:2]
    if fdlist:
        return fdlist[0]

def feed_import_rm(id, current_user_id):
    part_time_job_new(PRIVILEGE_FEED_IMPORT, id, current_user_id)
    feed_state_set(id, FEED_IMPORT_STATE_RM)


def feed_state_set(id, state):
    feed = FeedImport.get(id)
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




def feed_review(id,  cid, title, txt, tag_id_list, current_user_id, author_rm=False, sync=False):
    feed = FeedImport.get(id)
    if feed and feed.state==FEED_IMPORT_STATE_INIT :
        if author_rm:
            if sync:
                feed.state = FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR_SYNC
            else:
                feed.state = FEED_IMPORT_STATE_REVIEWED_WITHOUT_AUTHOR
        else:
            if sync:
                feed.state = FEED_IMPORT_STATE_REVIEWED_SYNC
            else:
                feed.state = FEED_IMPORT_STATE_REVIEWED

        feed.cid = int(cid)
        feed.title = title
        feed.txt = txt
        feed.tag_id_list = tag_id_list
        
        part_time_job_new(PRIVILEGE_FEED_IMPORT, feed.id, current_user_id)

        feed.save()


if __name__ == '__main__':
    pass
 
    #feed_import_by_douban_feed()
    #print FeedImport.where(state = FEED_IMPORT_STATE_INIT)
    #feed2po_new()

    #    i.txt = i.txt.replace("豆友","网友").replace("豆油","私信").replace("豆邮","私信")
    #    i.tag_id_list = ""
    #    print i.id, i.tag_id_list
    #    i.save()
    #print FeedImport.where(state=FEED_IMPORT_STATE_INIT)[:2]
    #print FeedImport.get(state = FEED_IMPORT_STATE_INIT)
    #print hot(2,0,1310424775)
