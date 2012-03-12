#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ctrl._urlmap.j import urlmap
from _handler import JLoginZsiteBase, JLoginBase
from model.cid import CID_TAG
from zkit.page import page_limit_offset, Page
from json import dumps
from model.po_tag import po_tag_by_cid, tag_cid_count, po_tag_new_by_autocompelte 
from model.tag_exp import tag_exp_new, tag_exp_state_txt_by_user_id_tag_id, tag_exp_new_apply_for_admin
from model.po import Po
from model.po_tag import tag_name_id_list_by_po_id
from json import loads
PAGE_LIMIT = 12 

@urlmap('/j/tag/(\d+)-(\-?\d+)')
class TagMore(JLoginZsiteBase):
    def get(self, cid, n):
        zsite_id = self.zsite_id        
        current_user_id = self.current_user_id

        page, limit, offset = page_limit_offset(
            'javascript:tag_cid_page(%s,%%s)'%cid,
            int(tag_cid_count(zsite_id, cid) or 0),
            n,
            PAGE_LIMIT
        )
        page = str(page) or 0
        #print int(tag_cid_count(zsite_id, cid) or 0)
 
        self.finish({
'li':po_tag_by_cid(cid, zsite_id, current_user_id, limit, offset),
'page':page

        })


@urlmap('/j/tag/manage/apply')
class TagManageApply(JLoginZsiteBase):
    def post(self):
        txt = self.get_argument('txt')
        user_id = self.current_user_id
        tag_id = self.zsite_id
        tag_exp_new_apply_for_admin(user_id, tag_id, txt)
        self.finish('{}') 

    def get(self):
        user_id = self.current_user_id
        tag_id = self.zsite_id
        self.finish(
            dumps(
                tag_exp_state_txt_by_user_id_tag_id(
                    user_id, tag_id
                )
            )
        )

@urlmap("/j/tag/po/(\d+)")
class TagPo(JLoginBase):
    def post(self, id):
        tag_id_list = self.get_argument('tag_id_list', '[]') 
        #print 'dasdasddasdasd',tag_id_list
        tag_id_list = map(str,loads(tag_id_list))
        user_id = self.current_user_id
        po = Po.mc_get(id) 
        result = {}

        if po:
            po_tag_new_by_autocompelte(po, tag_id_list, admin_id=user_id)
            tag_list = tag_name_id_list_by_po_id(id)
            result['tag_list'] = tag_list
        
        self.finish(result)


