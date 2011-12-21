#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from tornado import httpclient
import tornado.web
import logging
from model.zsite_book import zsite_book_new, zsite_book_id_by_isbn, ZsiteBook, Zsite, zsite_book_lib_new, zsite_book_lib, ZsiteBookLib



@urlmap('/book/lib/(\d+)')
class BookLib(Base):
    def get(self, id):
        booklib = ZsiteBookLib.mc_get(id)
        book = ZsiteBook.mc_get(booklib.book_id)
        self.render(booklib=booklib, book=book)

@urlmap('/book-(\d+)')
class ZsiteBookPage(Base):
    def get(self, n):
        self.render(page_list=zsite_book_lib()) 

@urlmap('/book')
class Index(Base):
    def get(self):
        self.render() 

@urlmap("/j/book/isbn/(\d+)")
class BookIsbn(Base):
    def get(self, isbn):
        id = zsite_book_id_by_isbn(isbn)
        result = {}
        if id:
            result['id']=id
        self.finish(result)


@urlmap("/book/(\d+)")
class Book(Base):
    def get(self, id):
        self.render() 

@urlmap("/book/new/(\d+)")
class BookNew(Base):
    def get(self,id):
        book = ZsiteBook.mc_get(id)
        if not book:
            return self.redirect("/")
        self.render(book=book)

    def post(self, id):
        total = self.get_argument('total',0)
        if total.isdigit():
            total = int(total)
            zsite_book_lib_new(id, total)
        return self.redirect("/book")

@urlmap("/book/new/douban/(\d+)")
class BookNewDouban(Base):
    def post(self, douban_id):
        name =  self.get_argument('title', '无题') 
        pic_id = self.get_argument('pic_id', 0)
        author = self.get_argument('author','')
        translator = self.get_argument('translator','')
        pages = self.get_argument('pages','')
        publisher = self.get_argument('publisher','')

        isbn = self.get_argument('isbn',0)
        rating = self.get_argument('rating','')
        rating_num = self.get_argument('rating_num','')

        author_intro = self.get_argument('author-intro','')
        txt = self.get_argument('txt','')

        id = zsite_book_new(
            name, douban_id, pic_id,
            author, translator, pages,  
            publisher, isbn,
            int(float(rating)*100), rating_num,
            author_intro, txt
        )

        self.finish({"id":id})






