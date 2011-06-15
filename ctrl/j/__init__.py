#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _handler
from ctrl.j._urlmap import urlmap


@urlmap('/j/login')
class Login(_handler.Base):
    def get(self):
        self.render()


