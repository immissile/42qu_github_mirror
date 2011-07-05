#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.google_plus import google_uid_by_link, GOOGLE_PLUS_URL, google_rank_new_by_html, google_rank_by_uid
from tornado import httpclient
import tornado.web

@urlmap('/google_plus')
class Index(Base):
    @tornado.web.asynchronous
    def get(self):
        q = self.get_argument('q', None)
        rank = None
        if q:
            uid = google_uid_by_link(q)
            if uid:
                rank = google_rank_by_uid(uid)
                print rank
                if not rank: 
                    self.uid = uid
                    client = httpclient.AsyncHTTPClient()
                    client.fetch(GOOGLE_PLUS_URL%q, self._callback)
                    return
        return self.render(q=q, rank=rank)


    def _callback(self, response):
        if response.error:
            print "Error:", response.error
        else:
            rank = google_rank_new_by_html(self.uid, response.body)
            return self.render(rank=rank)


