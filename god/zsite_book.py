#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from tornado import httpclient
import tornado.web
import logging
from model.zsite_book import zsite_book_new, zsite_book_id_by_isbn, ZsiteBook, Zsite, zsite_book_lib_new, zsite_book_lib, ZsiteBookLib
from model.user_mail import user_id_by_mail
from model.user_new import user_new
from model.zsite import Zsite

@urlmap('/book/lib/(\d+)')
class BookLib(Base):
    def get(self, id):
        booklib = ZsiteBookLib.mc_get(id)
        book = ZsiteBook.mc_get(booklib.book_id)
        self.render(booklib=booklib, book=book)

    def post(self, id):
        booklib = ZsiteBookLib.mc_get(id)
        book = ZsiteBook.mc_get(booklib.book_id)

        if booklib.is_exist:
            mail = self.get_argument("mail","")
            mail = mail.strip().lower()
            if mail:
                user_id = user_id_by_mail(mail)
                if not user_id:
                    user_id = user_new(mail)
                return self.redirect(
                    '/book/lib/browse/%s/%s'%(id, user_id)
                )
        return self.get(id)       

 
@urlmap('/book/lib/browse/(\d+)/(\d+)')
class BookLibBrowse(Base):
    def get(self, id, user_id):
        booklib = ZsiteBookLib.mc_get(id)
        book = ZsiteBook.mc_get(booklib.book_id)
        if not booklib.is_exist:
            return self.redirect("/book/lib/%s"%id)

        zsite = Zsite.mc_get(zsite) 
        self.render(booklib=booklib, book=book, zsite=zsite)

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






