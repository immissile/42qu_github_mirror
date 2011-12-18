#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _db
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA, McLimitA
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE, Zsite, ZSITE_STATE_VERIFY
from model.cid import CID_BOOK

mc_zsite_book_id_by_isbn = McCache("ZsiteBookIdByIsbn:%s")

class ZsiteBook(McModel):
    pass

def name_join(name_list):
    return ';'.join(i.replace(";","-") for i in name_list)

def name_split(name_list):
    return name_list.split(";")

@mc_zsite_book_id_by_isbn("{isbn}")
def zsite_book_id_by_isbn(isbn):
    isbn_len = len(str(isbn))
    if  isbn_len == 10:
        isbn = isbn10to13(isbn) 

    ZsiteBook.get(isbn=isbn)
    if book:
        return book.id


def zsite_book_new(
    name, 
    douban_id,
    pic_id,
    author, tranlator, pages,
    publisher,  isbn, 
    rating, rating_num,
    author_intro, txt,
):
    if douban_id:
        if ZsiteBook.get(douban_id=douban_id):
            return
    if isbn and zsite_book_id_by_isbn(isbn):
        return
    zsite = zsite_new(name, CID_BOOK)
    id = zsite.id
    book = ZsiteBook.get_or_create(id=id)
    book.author = author
    book.tranlator = tranlator 



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
    print isbn10to13(7543639130)
