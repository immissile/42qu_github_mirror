#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.buzz_sys import BuzzSys, buzz_sys_init_id_list, buzz_sys_init_list, buzz_sys_list, buzz_sys_count, buzz_sys_new, buzz_sys_edit, mc_buzz_sys_init_id_list
from zkit.page import page_limit_offset


@urlmap('/buzz/sys/new')
class SysNew(Base):
    def get(self):
        self.render()

    def post(self):
        htm = self.get_argument('htm', None)
        if not htm:
            return self.get()
        buzz_sys_new(htm)
        self.redirect('/buzz/sys')

@urlmap('/buzz/sys/(\d+)')
class SysEdit(Base):
    def get(self, id):
        s = BuzzSys.mc_get(id)
        if s:
            self.render(s=s)

    def post(self, id):
        s = BuzzSys.mc_get(id)
        if s:
            htm = self.get_argument('htm', None)
            seq = self.get_argument('seq', None)
            seq = int(seq)
            if not htm and seq:
                return self.get(id)
            buzz_sys_edit(id, htm, seq)
            self.redirect('/buzz/sys')

PAGE_LIMIT = 42

@urlmap('/buzz/sys(?:-(\d+))?')
class SysList(Base):
    def get(self, n=1):
        total = buzz_sys_count()
        page, limit, offset = page_limit_offset(
            '/buzz/sys-%s',
            total,
            n,
            PAGE_LIMIT,
        )
        li = buzz_sys_list(limit, offset)
        self.render(
            li=li,
            page=page,
        )


@urlmap('/buzz/sys/init')
class SysListInit(Base):
    def get(self):
        li = buzz_sys_init_list()
        self.render(li=li)

    def post(self):
        id_list = buzz_sys_init_id_list()
        li = [(id, int(self.get_argument('seq%s' % id, 0))) for id in id_list]
        li = filter(bool, li)
        li.sort(key=lambda x:x[1])
        for seq, (id, _) in enumerate(li, 1):
            s = BuzzSys.mc_get(id)
            s.seq = seq
            s.save()
            mc_buzz_sys_init_id_list.delete('')
        self.redirect('/buzz/sys/init')
