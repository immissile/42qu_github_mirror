#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl.main._handler import Base


class JLoginBase(Base):
    def prepare(self):
        super(JLoginBase, self).prepare()
        if not self.current_user:
            self.finish('{"login":1}')
    
    def post(self):
        return self.get()
