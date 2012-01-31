#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.import_feed import ImportFeed, get_feed_2_edit, allow_feed
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

        allow_feed(id,sync)
        print id,title,sync,delauthor

        _get(self,next)


