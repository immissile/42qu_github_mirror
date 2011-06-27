#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.buzz_sys import buzz_sys_init_list, buzz_sys_list, buzz_sys_count, buzz_sys_new, buzz_sys_edit
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
        self.render(**vars())


@urlmap('/buzz/sys/init')
class SysListInit(Base):
    def get(self):
        li = buzz_sys_init_list()
        self.render(**vars())
