#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _db
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA, McLimitA
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE, Zsite, ZSITE_STATE_VERIFY
from model.cid import CID_BOOK
from txt import txt_new



mc_zsite_book_id_by_isbn = McCache('ZsiteBookIdByIsbn:%s')

# CREATE TABLE `zpage`.`zsite_book_lib` (
#   `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#   `book_id` INTEGER UNSIGNED NOT NULL,
#   `from_id` INTEGER UNSIGNED NOT NULL DEFAULT 0,
#   `state` INTEGER UNSIGNED NOT NULL DEFAULT 0,
#   `pid` INTEGER UNSIGNED NOT NULL DEFAULT 0,
#   `address_id` INTEGER UNSIGNED NOT NULL DEFAULT 0,
#   PRIMARY KEY (`id`),
#   INDEX `Index_2`(`from_id`),
#   INDEX `Index_3`(`book_id`, `state`)
# )

ZSITE_BOOK_LIB_STATE_EXIST = 10

class ZsiteBookLib(McModel):
    pass

class ZsiteBook(McModel):
    pass

def name_join(name_list):
    return ';'.join(i.replace(';', '-') for i in name_list)

def name_split(name_list):
    return name_list.split(';')

@mc_zsite_book_id_by_isbn('{isbn}')
def zsite_book_id_by_isbn(isbn):
    isbn_len = len(str(isbn))
    if  isbn_len == 10:
        isbn = isbn10to13(isbn)
        isbn_len = 13
    if isbn_len == 13:
        book = ZsiteBook.get(isbn=isbn)
        if book:
            return book.id

    return 0

def zsite_book_lib():
    l = list(ZsiteBookLib.where())
    Zsite.mc_bind(l, 'zsite', 'book_id')
    return l

def zsite_book_by_lib(book_id):
    l = ZsiteBookLib.where(book_id=book_id).col_list()
    return l

def zsite_book_lib_new(book_id, total):
    if not ZsiteBook.mc_get(book_id):
        return
    for i in range(total):
        book = ZsiteBookLib(
            book_id=book_id,
            state=ZSITE_BOOK_LIB_STATE_EXIST
        )
        book.save()


def zsite_book_new(
    name,
    douban_id,
    pic_id,
    author, translator, pages,
    publisher, isbn,
    rating, rating_num,
    author_intro, txt,
):
    if douban_id:
        book = ZsiteBook.get(douban_id=douban_id)
        if book:
            return book.id
    if isbn:
        book_id = zsite_book_id_by_isbn(isbn)
        if book_id:
            return book_id
    zsite = zsite_new(name, CID_BOOK)
    id = zsite.id
    if isbn:
        mc_zsite_book_id_by_isbn.set(isbn, id)

    txt_new(id, txt)
    book = ZsiteBook.get_or_create(id=id)
    book.douban_id = douban_id
    book.douban_pic_id = pic_id
    book.author = author
    book.translator = translator
    book.pages = pages
    book.publisher = publisher
    book.isbn = isbn
    book.rating = rating
    book.rating_num = rating_num
    book.author_intro = author_intro
    #print author_intro,"author_intro"
    book.save()
    return id

def isbn10to13(number):
    number = str(number)
    number = '978'+number[:9]+'0'
    lc = len(number)
    if lc < 12 or lc > 13:
        return None
    if lc == 12:
        number = '0'+number
    p = 0
    for i in range(0, 12, 2):
        p = p+int(number[i])
    for i in range(1, 12, 2):
        p = p+int(number[i])*3
    p = (10-(p % 10))%10
    if p == int(number[12]):
        return number
    else:
        return number[:12]+str(p)


if __name__ == '__main__':
    #for j, i in enumerate(Zsite.where(cid=CID_COM)):
    #print i.name, j
    #print isbn10to13(7543639130)
    pass
