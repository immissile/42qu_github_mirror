#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.zsite._handler import LoginBase, XsrfGetBase
from ctrl._urlmap.zsite import urlmap
from _handler import AdminBase

@urlmap('/resume/confirm')
class ResumeConfirm(AdminBase):
    def get(self):
        return self.render()

@urlmap('/resume/(\d+)')
class Resume(AdminBase):
    def get(self, id):
        return self.render()


