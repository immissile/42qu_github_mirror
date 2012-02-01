#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.site_sync import site_sync_rm, site_sync_new
from model.import_feed import ImportFeed, get_feed_2_edit, feed_2_po , rm_import_feed
from model.rec_read import rec_cid_push
from yajl import dumps

@urlmap('/import_feed')
class ImportFeed(Base):
    def get(self):
        self.render()


def _get(self):
    feed = get_feed_2_edit()
    if feed:
        result = {
            'id':feed.id,
            'title':feed.title,
            'txt':feed.txt,
            'tags':[],
        }
        self.finish(dumps(result))

@urlmap('/import_feed/next')
class ImportFeedShow(Base):
    get = _get

    def post(self):
        id = self.get_argument('id',None)
        title = self.get_argument('title',None)
        txt = self.get_argument('txt',None)
        sync = self.get_argument('sync',None)
        delauthor = self.get_argument('delauthor',None)
        cid = self.get_argument('cid',None)

        po = feed_2_po(id,delauthor)
        if po and cid:
            print cid,po.id
            rec_cid_push(cid, po.id)

        if sync:
            #site_sync(po.id)
            pass

        print id,title,sync,delauthor
        self.get()

@urlmap('/import_feed/rm')
class ImportFeedRm(Base):
    def post(self):
        id = self.get_argument('id',None)
        rm_import_feed(id)
        _get(self)

