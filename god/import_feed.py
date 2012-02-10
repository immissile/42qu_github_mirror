#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.site_sync import site_sync_rm, site_sync_new
from model.feed_import import FeedImport, feed_next, review_feed , feed_import_rm, po_tag_new
from model.douban import is_rt_by_title 
from model.po_by_tag import tag_list_by_po_id
from zkit.page import page_limit_offset
from model.po import Po, po_rm
from yajl import dumps

@urlmap('/feed_import')
class FeedImport(Base):
    def get(self):
        self.render()


def _get(self):
    feed = feed_next()
    if feed:
        author_rm = is_rt_by_title(feed.title)
        result = {
            'id':feed.id,
            'title':feed.title,
            'txt':feed.txt,
            'tags':[(tag,0) for tag in feed.tags.split(',')],
            'author_rm':author_rm,
            'url':feed.url
        }
        self.finish(dumps(result))

@urlmap('/feed_import/next')
class FeedImportShow(Base):
    get = _get

    def post(self):
        id = self.get_argument('id', None)
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        sync = self.get_argument('sync', None)
        author_rm = self.get_argument('author_rm', None)
#        cid = self.get_argument('cid', None)
        tags = self.get_argument('tags', '')

        current_user_id = self.current_user_id
        review_feed(id,  title, txt, tags,current_user_id, author_rm, sync)

        self.get()

@urlmap('/feed_import/rm')
class FeedImportRm(Base):
    def post(self):
        id = self.get_argument('id', None)
        current_user_id = self.current_user_id

        feed_import_rm(id, current_user_id)
        _get(self)


@urlmap('/feed_import/edit/(\d+)')
@urlmap('/feed_import/(\d+)/edit/(\d+)')
class FeedImportEdit(Base):
    def get(self, cid=0, id=0):
        id = int(id)
        cid = int(cid)
        if  id:
            po = Po.mc_get(id)
            if po:
                tags = tag_list_by_po_id(po.id)
                self.render(po=po, cid=cid, tags=tags)
        else:
            self.redirect('/feed_import/list/1')

    def post(self, old_cid=0):
        old_cid = int(old_cid)
        id = int(self.get_argument('id', None))
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        sync = self.get_argument('sync', None)
        author_rm = self.get_argument('author_rm', None)
        cid = self.get_argument('cid', None)
        tags = self.get_argument('tags', '')

        po = Po.mc_get(id)
        if po:
            if author_rm:
                po.rid = 0
                po.zsite_id = 0
            if sync:
                site_sync_new(po.id)
            po.txt_set(txt)
            po.name_ = title
            if cid:
                rec_cid_mv(po.id, old_cid, int(cid))

            po.save()
            po_tag_new(tags, po)

        self.redirect('/feed_import/list/%s'%old_cid)

            
