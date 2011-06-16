#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
import _handler
from ctrl._urlmap.j import urlmap


@urlmap('/j/login')
class Login(Base):
    def get(self):
        self.render()
