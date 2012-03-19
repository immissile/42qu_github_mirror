#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.google_plus import google_uid_by_link, google_rank_new_by_html, google_rank_by_uid, GoogleRank, GOOGLE_PLUS_URL_PROXY
from zkit.page import page_limit_offset
from tornado import httpclient
import tornado.web


@urlmap('/google_plus')
@urlmap('/google_plus-(\d+)')
class Index(Base):
    @tornado.web.asynchronous
    def get(self, n=1):
        q = self.get_argument('q', None)
        rank = None
        if q:
            uid = google_uid_by_link(q)
            if uid:
                rank = google_rank_by_uid(uid)
                if not rank:
                    self.uid = uid
                    client = httpclient.AsyncHTTPClient()
                    url = GOOGLE_PLUS_URL_PROXY%uid
                    #logging.info(url)
                    client.fetch(url, self._callback)
                    return

        self._page(n, rank, q)

    def _callback(self, response):
        if response.error:
            print 'Error:', response.error
        else:
            html = response.body
            if html:
                uid = self.uid
                rank = google_rank_new_by_html(uid, html)
                return self._page(1, rank, uid)
            return self.get()

    def _page(self, n, rank, q):
        page, limit, offset = page_limit_offset(
            '/google_plus-%s',
            GoogleRank.count(),
            n,
            50,
        )
        rank_list = GoogleRank.mc_get_list(GoogleRank.where().order_by('follower desc').col_list(limit, offset))

        return self.render(
            q=q, rank=rank, page=page, rank_list=rank_list, offset=offset
        )


