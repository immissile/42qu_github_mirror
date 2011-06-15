#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
import _handler
from zweb._urlmap import urlmap


@urlmap('/j/login')
class Login(Base):
    def get(self):
        self.render()
