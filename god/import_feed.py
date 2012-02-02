#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.site_sync import site_sync_rm, site_sync_new
from model.import_feed import ImportFeed, feed_next, review_feed , import_feed_rm, apply_tag
from model.rec_read import rec_cid_push, rec_id_by_cid, rec_change
from model.douban import title_normal
from model.po_by_tag import tag_list_by_po_id
from model.po import Po
from yajl import dumps
from model.po import Po

@urlmap('/import_feed')
class ImportFeed(Base):
    def get(self):
        self.render()


def _get(self):
    feed = feed_next()
    if feed:
        del_author = feed.title != title_normal(feed.title)
        result = {
            'id':feed.id,
            'title':feed.title,
            'txt':feed.txt,
            'tags':[],
            'del_author':True if del_author else False
        }
        self.finish(dumps(result))

@urlmap('/import_feed/next')
class ImportFeedShow(Base):
    get = _get

    def post(self):
        id = self.get_argument('id', None)
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        sync = self.get_argument('sync', None)
        author_rm = self.get_argument('author_rm', None)
        cid = self.get_argument('cid', None)
        tags = self.get_argument('tags', None)

        print tags
        review_feed(id, cid, title, txt, tags, author_rm, sync)

        self.get()

@urlmap('/import_feed/rm')
class ImportFeedRm(Base):
    def post(self):
        id = self.get_argument('id', None)
        import_feed_rm(id)
        _get(self)

@urlmap('/import_feed/list/(\d+)')
class ImportFeedList(Base):
    def get(self, n=1):
        n = int(n)
        id_list = rec_id_by_cid(n)
        po_list = Po.mc_get_list(id_list)
        self.render(
                items=po_list,
                cid=n
                )
@urlmap('/import_feed/edit/(\d+)')
@urlmap('/import_feed/(\d+)/edit/(\d+)')
class ImportFeedEdit(Base):
    def get(self, cid=0, id=0):
        id = int(id)
        cid = int(cid)
        if  id:
            po = Po.mc_get(id)
            if po:
                tags = tag_list_by_po_id(po.id)
                self.render(po=po, cid=cid, tags=tags)
        else:
            self.redirect('/import_feed/list/1')

    def post(self, old_cid=0):
        old_cid = int(old_cid)
        id = int(self.get_argument('id', None))
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        sync = self.get_argument('sync', None)
        author_rm = self.get_argument('author_rm', None)
        cid = self.get_argument('cid', None)
        tags = self.get_argument('tags', None)

        po = Po.mc_get(id)
        if po:
            if author_rm:
                po.rid = 0
            if sync:
                site_sync_new(po.id)
            po.txt_set(txt)
            po.name_ = title
            if cid:
                rec_change(po.id, old_cid, int(cid))




#self.write('%s,%s,%s,%s'%(id,title,cid,tags))
