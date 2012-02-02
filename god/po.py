#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.zsite import Zsite
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.cid import CID_PO, CID_WORD, CID_NOTE, CID_QUESTION, CID_CHANNEL, CID_REC
from model.po import Po, po_state_set, po_rm
from model.po_show import po_show_new, po_show_count, po_show_list, po_show_rm
from model.state import STATE_RM, STATE_SECRET, STATE_ACTIVE, STATE_PO_ZSITE_SHOW_THEN_REVIEW
from zkit.page import page_limit_offset
from model.god_po_show import mc_po_show_zsite_channel
from model.site_sync import site_sync_rm, site_sync_new
from model.spammer import spammer_reset, spammer_new
from zkit.txt import format_txt


PAGE_LIMIT = 50

@urlmap('/po(?:-(\d+))?')
class PoList(Base):
    def get(self, n=1):
        qs = Po.where('state>%s', STATE_RM).where('zsite_id!=user_id').where('user_id!=0')
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/po-%s',
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        Po.mc_bind(li, 'question', 'rid')
        self.render(
            po_list=li,
            page=page,
        )


@urlmap('/po/zsite(?:-(\d+))?')
class PoList(Base):
    def get(self, n=1):
        qs = Po.where('state>%s', STATE_RM).where('zsite_id=user_id')
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/po/zsite-%s',
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        Po.mc_bind(li, 'question', 'rid')
        self.render(
            po_list=li,
            page=page,
        )

@urlmap('/po/edit/(\d+)')
class PoEdit(Base):
    def get(self, id):
        po = Po.mc_get(id)
        next = self.request.headers.get('Referer', '')
        self.render(po=po, next=next)

    def post(self, id):
        po = Po.mc_get(id)
        next = self.get_argument('next', '/po')
        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)
        if name:
            po.name_ = name
            po.save()
        if txt:
            po.txt_set(txt)
        self.redirect(next)




@urlmap('/po/state/(\d+)/(%s|%s)' % (STATE_SECRET, STATE_ACTIVE))
class PoState(Base):
    def post(self, id, state):
        po = Po.mc_get(id)
        state = int(state)
        if po:
            po_state_set(po, state)
        self.finish('{}')


@urlmap('/po/show(?:-(\d+))?')
class PoShow(Base):
    template = '/god/po/po_list.htm'

    def get(self, n):
        page, limit, offset = page_limit_offset(
            '/po/show-%s',
            po_show_count(),
            n,
            PAGE_LIMIT,
        )
        li = po_show_list(limit, offset)
        self.render(
            po_list=li,
            page=page,
        )

@urlmap('/po/show/rm/(\d+)')
class PoShowRm(Base):
    def get(self, id):
        po_show_rm(id)
        next = self.request.headers.get('Referer', '/po/show/set/%s'%id)
        self.redirect(next)

@urlmap('/po/sync/rm/(\d+)')
class PoSyncRm(Base):
    def get(self, id):
        site_sync_rm(id)
        self.redirect('/po/show/set/%s'%id)



def _edit(broad,sync,site,po,id):
    if broad:
        from model.po_recommend import po_recommend_new
        test_po = Po.get(rid =po.id,user_id = 0, state = STATE_ACTIVE)
        if not test_po:
            po_recommend_new(po.id,0,'')
    else:
        po_show_rm(po)

    if sync:
        site_sync_new(id)
    else:
        site_sync_rm(id)

    if site:
        po.zsite_id_set(site)


@urlmap('/po/show/edit/(\d+)')
class PoEditShow(Base):
    def get(self,id):
        next = self.request.headers.get('Referer', '')
        po = Po.mc_get(id)
        if po:
            self.render(
                po=po,
                next=next,
            )
    

    def post(self,id):
        po = Po.mc_get(id)
        next = self.get_argument('next', '/po')
        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)
        broad = self.get_argument('broad', None)
        site = self.get_argument('site', None)
        sync = self.get_argument('sync', None)
        _format = self.get_argument('format',None)
        _edit(broad,sync,site,po,id) 
        if name:
            po.name_ = name
            po.save()
        if txt:
            if _format:
                txt = format_txt(txt)
            po.txt_set(txt)
       
        self.redirect(next)



@urlmap('/po/show/set/(\d+)')
class PoShowSet(Base):
    def get(self, id):
        next = self.request.headers.get('Referer', '')
        po = Po.mc_get(id)
        if po:
            self.render(
                po=po,
                next=next,
            )

    def post(self, id):
        po = Po.mc_get(id)
        next = self.get_argument('next', '/po')
        broad = self.get_argument('broad', None)
        site = self.get_argument('site', None)
        sync = self.get_argument('sync', None)
        if po:
            _edit(broad,sync,site,po,id)
            return self.redirect(next)

        self.render(
            po=po,
            next=next,
        )



@urlmap('/rm/(\d+)')
class Rm(Base):
    def get(self,po_id):
        p = Po.mc_get(po_id)
        if p:
            user = p.user
            if user or not p.user_id:
                self.render(user=user)

    def post(self,po_id):
        add = self.get_argument('add_spammer',None)
        del_all = self.get_argument('del_all',None)
        p = Po.mc_get(po_id)
        if p:
            user = p.user
            if user:
                user_id = user.id
            else:
                user_id = 0

            if add:
                spammer_new(user_id)
            
            if del_all:
                spammer_reset(user_id)

            po_rm(user_id,po_id)
       
       
        self.redirect('/po')
