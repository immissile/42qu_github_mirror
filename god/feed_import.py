#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _handler import Base
from _urlmap import urlmap
from model.site_sync import site_sync_rm, site_sync_new
from model.feed_import import FeedImport,  feed_review , feed_import_rm, FEED_IMPORT_STATE_INIT
from model.po_by_tag import po_tag_new_by_autocompelte
from model.douban import is_rt_by_title 
from model.po_by_tag import tag_list_by_po_id
from zkit.page import page_limit_offset
from model.po import Po, po_rm
from tornado.escape import json_encode 
from yajl import dumps
from model.zsite import Zsite
from zkit.page import limit_offset, Page
from model.tag_admin import tag_id_name_count_list_by_tag_admin , id_by_tag_admin

@urlmap('/feed_import')
@urlmap('/feed_import-(\d+)')
class TagList(Base):
    def get(self, n=1):

        page_limit = 200
        now, list_limit, offset = limit_offset(
            n,
            page_limit
        )
        tag_id_name_count_list, count = tag_id_name_count_list_by_tag_admin(list_limit, offset)
        tag_id_name_count_list, count = ([(10230364L, '\xe8\xb6\x85\xe6\x96\x87\xe6\x9c\xac\xe4\xbc\xa0\xe8\xbe\x93\xe5\x8d\x8f\xe8\xae\xae / HTTP', 82), (10225558L, '\xe5\xa7\x91\xe5\xa8\x98', 21), (10234095L, '\xe7\xbb\x93\xe5\xa9\x9a', 19), (10228760L, '\xe7\x94\xb7\xe6\x9c\x8b\xe5\x8f\x8b', 17), (10232537L, '\xe5\x88\x86\xe6\x89\x8b', 15), (10225648L, '\xe5\x90\xb5\xe6\x9e\xb6', 15), (10230496L, '\xe8\xb1\x86\xe7\x93\xa3', 13), (10232202L, '\xe7\x94\xb5\xe5\xbd\xb1', 12), (10226319L, '\xe9\x98\x85\xe8\xaf\xbb', 12), (10233046L, '\xe6\x98\x9f\xe5\xba\xa7\xe5\x88\x86\xe6\x9e\x90', 11), (10232047L, '\xe8\x85\xbe\xe8\xae\xaf IM', 11), (10231600L, '\xe5\xbe\xae\xe5\x8d\x9a', 11), (10231077L, '\xe7\x94\xb5\xe6\xa2\xaf', 11), (10221330L, '\xe5\xa5\xb3\xe6\x9c\x8b\xe5\x8f\x8b', 11), (10220839L, '\xe6\x98\x9f\xe5\xba\xa7', 11), (10232303L, '\xe5\xa6\x88\xe5\xa6\x88', 10), (10231235L, '\xe5\x90\x83\xe9\xa5\xad', 10), (10230740L, '\xe5\xb0\x8f\xe4\xb8\x89', 10), (10226718L, '\xe5\x8d\x97\xe4\xba\xac', 10), (10223752L, '\xe5\x9b\x9e\xe5\xae\xb6', 10), (10223006L, '\xe5\xa4\xa9\xe7\xa7\xa4\xe5\xba\xa7 / \xe5\xa4\xa9\xe5\xb9\xb3\xe5\xba\xa7', 10), (10220877L, '\xe7\x88\xb1\xe6\x83\x85', 10), (10231647L, '\xe5\x8f\x8c\xe9\xb1\xbc\xe5\xba\xa7', 9), (10229648L, '\xe8\xa1\xa3\xe6\x9c\x8d', 9), (10229504L, '\xe5\xb7\xa8\xe8\x9f\xb9\xe5\xba\xa7', 9), (10228558L, 'Weibo', 9), (10225510L, '\xe6\x9c\x8b\xe5\x8f\x8b', 9), (10225361L, '\xe5\x90\x83\xe4\xb8\x9c\xe8\xa5\xbf', 9), (10225249L, '\xe5\x87\x8f\xe8\x82\xa5', 9), (10224176L, '\xe5\x8e\xa6\xe9\x97\xa8', 9), (10223360L, 'HTML 4.01', 9), (10233612L, '\xe8\xb0\x88\xe6\x81\x8b\xe7\x88\xb1', 8), (10232452L, '\xe7\x9b\xb8\xe5\x86\x8c', 8), (10231313L, '\xe5\x90\x90\xe6\xa7\xbd', 8), (10230065L, '\xe5\xa5\xbd\xe5\x90\x83', 8), (10228176L, '\xe8\x8b\xb9\xe6\x9e\x9c / Apple Inc.', 8), (10227262L, 'renren', 8), (10227118L, '\xe5\xa9\x9a\xe5\xa7\xbb', 8), (10226418L, '\xe8\x83\x8c\xe5\x8d\x95\xe8\xaf\x8d', 8), (10226391L, '\xe7\xa7\x81\xe4\xbf\xa1', 8), (10221659L, '\xe7\x88\xb6\xe6\xaf\x8d', 8), (10233851L, '\xe7\xbd\x91\xe7\xab\x99', 7), (10232070L, '\xe5\xbc\x82\xe5\x9c\xb0\xe6\x81\x8b', 7), (10230669L, '\xe5\xad\xa9\xe5\xad\x90', 7), (10229419L, 'Backbone.js', 7), (10228259L, '\xe9\xbb\x91\xe7\x9c\xbc\xe5\x9c\x88', 7), (10227811L, '\xe7\x99\xbd\xe7\xbe\x8a\xe5\xba\xa7', 7), (10226630L, '\xe7\x81\xab\xe8\xbd\xa6\xe7\xa5\xa8', 7), (10225018L, '\xe5\x8f\x8c\xe5\xad\x90\xe5\xba\xa7', 7), (10223798L, '\xe8\xaf\xb4\xe8\xaf\x9d', 7)], 2319)

        page = str(Page(
            '/feed_import-%s',
            count,
            now,
            page_limit
        ))

        self.render(
            tag_id_name_count_list = tag_id_name_count_list,
            page = page 
        ) 

@urlmap("/feed_import/(\d+)")
class Tag(Base):
    def get(self, id):
        self.render(id=id) 

def _tag_feed_next(tag_id, offset):
    feed_id = id_by_tag_admin(tag_id, offset)
    #feed_id = 1
    if feed_id:
        feed = FeedImport.get(feed_id)
        author_rm = is_rt_by_title(feed.title)
        tag_id_list = filter(bool,feed.tag_id_list.split(' '))
        tag_id_list = list(
            zip(
                [ i.name for i in Zsite.mc_get_list(tag_id_list) if i is not None], 
                tag_id_list
            )
        )

        r = {
            'id':feed.id,
            'title':feed.title,
            'txt':feed.txt,
            'tag_id_list':tag_id_list,
            'author_rm':author_rm,
            'url':feed.url
        }
    else:
        r = "0"
    return r 

@urlmap("/feed_import/(\d+)/(\d+)")
class FeedImportJson(Base):
    def get(self, tag_id, offset):
        self.finish(_tag_feed_next(tag_id, offset))

    def post(self, tag_id, offset):
        id = self.get_argument('id', None)
        title = self.get_argument('title', None)
        txt = self.get_argument('txt', None)
        sync = self.get_argument('sync', None)
        author_rm = self.get_argument('author_rm', None)
        tag_id_list = self.get_argument('tag_id_list', '')
        cid = self.get_argument('cid',None)

        current_user_id = self.current_user_id
        feed_review(id,  cid, title, txt, tag_id_list,current_user_id, author_rm, sync)
       
        self.get(tag_id, offset) 

@urlmap("/feed_import/(\d+)/rm/(\d+)")
class FeedImportRmJson(Base):
    def post(self, tag_id, id):
        current_user_id = self.current_user_id
        feed_import_rm(id, current_user_id)

        self.finish(_tag_feed_next(tag_id, 1))


#@urlmap('/feed_import')
#class Index(Base):
#    def get(self):
#        o = FeedImport.get(state = FEED_IMPORT_STATE_INIT)
#        self.render(result=_dumps_feed(o))


#def _get(self):
#    feed = feed_next()
#    result = _dumps_feed(feed)
#    self.finish(result)
#    
#
#def _dumps_feed(feed):
#    if feed:
#    else:
#        return {}
#
#
#@urlmap('/feed_import/next')
#class FeedImportShow(Base):
#    get = _get
#
#    def post(self):
#        id = self.get_argument('id', None)
#        title = self.get_argument('title', None)
#        txt = self.get_argument('txt', None)
#        sync = self.get_argument('sync', None)
#        author_rm = self.get_argument('author_rm', None)
#        tag_id_list = self.get_argument('tag_id_list', '')
#        cid = self.get_argument('cid',None)
#
#        current_user_id = self.current_user_id
#        feed_review(id,  cid, title, txt, tag_id_list,current_user_id, author_rm, sync)
#
#        self.get()
#
#@urlmap('/feed_import/rm')
#class FeedImportRm(Base):
#    def post(self):
#        _get(self)
#
#
#@urlmap('/feed_import/edit/(\d+)')
#@urlmap('/feed_import/(\d+)/edit/(\d+)')
#class FeedImportEdit(Base):
#    def get(self, cid=0, id=0):
#        id = int(id)
#        cid = int(cid)
#        if  id:
#            po = Po.mc_get(id)
#            if po:
#                tag_id_list = tag_list_by_po_id(po.id)
#                self.render(po=po, cid=cid, tag_id_list=tag_id_list)
#        else:
#            self.redirect('/feed_import/list/1')
#
#    def post(self, old_cid=0):
#        old_cid = int(old_cid)
#        id = int(self.get_argument('id', None))
#        title = self.get_argument('title', None)
#        txt = self.get_argument('txt', None)
#        sync = self.get_argument('sync', None)
#        author_rm = self.get_argument('author_rm', None)
#        cid = self.get_argument('cid', None)
#        tag_list = self.get_argument('tag_id_list', '')
#
#        po = Po.mc_get(id)
#        if po:
#            if author_rm:
#                po.rid = 0
#                po.zsite_id = 0
#            if sync:
#                site_sync_new(po.id)
#            po.txt_set(txt)
#            po.name_ = title
#            if cid:
#                rec_cid_mv(po.id, old_cid, int(cid))
#
#            po.save()
#            po_tag_new_by_autocompelte(po, tag_list)
#
#        self.redirect('/feed_import/list/%s'%old_cid)
#
            
