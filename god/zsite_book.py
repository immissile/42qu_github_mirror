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

@urlmap("/j/book/isbn")
class Isbn(Base):
    def get(self):
        self.finish("{}")

@urlmap("/book/(\d+)")
class Book(Base):
    def get(self, id):
        self.render() 

@urlmap("/book/new/(\d+)")
class BookNew(Base):
    def get(self,id):
        self.render()

@urlmap("/book/new/douban")
class BookNewDouban(Base):
    def post(self):
        id = 1
        self.finish({id:id})

