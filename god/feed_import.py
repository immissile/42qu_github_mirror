#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.site_sync import site_sync_rm, site_sync_new
from model.feed_import import FeedImport, feed_next, feed_review , feed_import_rm, FEED_IMPORT_STATE_INIT
from model.po_by_tag import po_tag_new_by_autocompelte
from model.douban import is_rt_by_title 
from model.po_by_tag import tag_list_by_po_id
from zkit.page import page_limit_offset
from model.po import Po, po_rm
from tornado.escape import json_encode 
from yajl import dumps
from model.zsite import Zsite


@urlmap('/feed_import/tag_list')
class Index(Base):
    def get(self):
        o = FeedImport.get(state = FEED_IMPORT_STATE_INIT)
        self.render(result=_dumps_feed(o))

@urlmap('/feed_import')
class Index(Base):
    def get(self):
        o = FeedImport.get(state = FEED_IMPORT_STATE_INIT)
        self.render(result=_dumps_feed(o))


def _get(self):
    feed = feed_next()
    result = _dumps_feed(feed)
    self.finish(result)
    

def _dumps_feed(feed):
    if feed:
        author_rm = is_rt_by_title(feed.title)
        tag_id_list = filter(bool,feed.tag_id_list.split(' '))
        tag_id_list = list(
            zip(
                [ i.name for i in Zsite.mc_get_list(tag_id_list) if i is not None], 
                tag_id_list
            )
        )

        result = {
            'id':feed.id,
            'title':feed.title,
            'txt':feed.txt,
            'tag_id_list':tag_id_list,
            'author_rm':author_rm,
            'url':feed.url
        }
        return json_encode(result)
    else:
        return {}


@urlmap('/feed_import/next')
class FeedImportShow(Base):
    get = _get

    def post(self):
        id = self.get_argument('id', None)
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        sync = self.get_argument('sync', None)
        author_rm = self.get_argument('author_rm', None)
        tag_id_list = self.get_argument('tag_id_list', '')
        cid = self.get_argument('cid',None)

        current_user_id = self.current_user_id
        feed_review(id,  cid, title, txt, tag_id_list,current_user_id, author_rm, sync)

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
                tag_id_list = tag_list_by_po_id(po.id)
                self.render(po=po, cid=cid, tag_id_list=tag_id_list)
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
        tag_list = self.get_argument('tag_id_list', '')

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
            po_tag_new_by_autocompelte(po, tag_list)

        self.redirect('/feed_import/list/%s'%old_cid)

            
