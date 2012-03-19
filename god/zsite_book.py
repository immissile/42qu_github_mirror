#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
import tornado.web
from model.zsite_book import zsite_book_new, zsite_book_id_by_isbn, ZsiteBook, Zsite, zsite_book_lib_new, zsite_book_lib, ZsiteBookLib, zsite_book_lib_browse, zsite_book_lib_return, ZSITE_BOOK_LIB_STATE_EXIST, zsite_book_lib_rm
from model.user_mail import user_id_by_mail
from model.user_new import user_new
from model.zsite import Zsite
from model.namecard import namecard_get

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
        elif booklib.is_browse:
            if self.get_argument("return",""):
                zsite_book_lib_return(id, self.current_user_id)
        return self.get(id)       

@urlmap('/book/lib/rm/(\d+)')
class BookLibRm(Base):
    def get(self, id):
        booklib = zsite_book_lib_rm(id)
        book = ZsiteBook.mc_get(booklib.book_id)
        return self.redirect("/book/new/%s"%booklib.book_id) 
 
@urlmap('/book/lib/browse/(\d+)/(\d+)')
class BookLibBrowse(Base):
    def _fetch(self, id , user_id):
        booklib = ZsiteBookLib.mc_get(id)
        book = ZsiteBook.mc_get(booklib.book_id)
        return book, booklib

    
    def get(self, id, user_id):
        book, booklib = self._fetch(id, user_id)
        zsite = Zsite.mc_get(user_id) 
        self.render(booklib=booklib, book=book, zsite=zsite)

    def post(self, id, user_id):
        book, booklib = self._fetch(id, user_id)
             
        zsite = Zsite.mc_get(user_id)
        namecard = namecard_get(user_id)
        zsite_name = self.get_argument('zsite_name','')
        name = self.get_argument('name','')
        phone = self.get_argument('phone','')
        days = self.get_argument('days','1')

        if zsite_name:
            zsite.name = zsite_name
            zsite.save()
        if phone:
            namecard.phone = phone
        if name:
            namecard.name = name
        if days and days.isdigit():
            days = int(days)
            zsite_book_lib_browse(id, user_id, days, self.current_user_id)

        namecard.save()
        self.redirect("/book/lib/%s"%id)



@urlmap('/book-(\d+)')
class ZsiteBookPage(Base):
    def get(self, n):
        self.render(page_list=zsite_book_lib(None,None,ZSITE_BOOK_LIB_STATE_EXIST )) 

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






