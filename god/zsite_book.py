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

@urlmap("/j/book/isbn/(\d+)")
class BookIsbn(Base):
    def get(self, isbn):
        self.finish("{}")


@urlmap("/book/(\d+)")
class Book(Base):
    def get(self, id):
        self.render() 

@urlmap("/book/new/(\d+)")
class BookNew(Base):
    def get(self,id):
        self.render()

@urlmap("/book/new/douban/(\d+)")
class BookNewDouban(Base):
    def post(self, douban_id):
        name =  self.get_argument('title', '无题') 
        pic_id = self.get_argument('pic_id', 0)
        author = self.get_argument('author',[])
        tranlator = self.get_argument('tranlator',[])
        pages = self.get_argument('pages','')
        publisher = self.get_argument('publisher','')

        rating = self.get_argument('rating','')
        rating_num = self.get_argument('rating_num','')

        author_intro = self.get_argument('author-intro','')
        txt = self.get_argument('txt','')

        print name, douban_id, pic_id, tranlator, author, pages,  publisher
        print rating, rating_num
        print txt, author_intro

        id = douban_id
        self.finish({"id":id})






