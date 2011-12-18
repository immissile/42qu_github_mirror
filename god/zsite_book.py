#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from tornado import httpclient
import tornado.web
import logging


@urlmap('/book')
class Index(Base):
    def get(self):
        self.render() 


