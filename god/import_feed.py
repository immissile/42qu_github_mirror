#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.site_sync import site_sync_rm, site_sync_new
from model.import_feed import ImportFeed, get_feed_2_edit, feed_2_po
from yajl import dumps

@urlmap('/import_feed')
class ImportFeed(Base):
    def get(self):
        self.render()
        

def _get(self,next=0):
    next = int(next)
    feed = get_feed_2_edit(next=next)
    if feed:
        result = {
                'id':feed.id,
                'title':feed.title,
                'body':feed.body,
                'tags':'empty',
                }
        self.finish(dumps(result))

@urlmap('/import_feed/next')
@urlmap('/import_feed/next/(0|1)')
class ImportFeedShow(Base):
    get = _get

    def post(self,next=0):
        id = self.get_argument('id',None)
        title = self.get_argument('title',None)
        body = self.get_argument('body',None)
        sync = self.get_argument('sync',None)
        delauthor = self.get_argument('delauthor',None)

        po = feed_2_po(id,delauthor)
        if sync:
            #site_sync(po.id)
            pass

        print id,title,sync,delauthor

        _get(self,next)


