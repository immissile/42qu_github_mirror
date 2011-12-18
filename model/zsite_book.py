#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _db
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA, McLimitA
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE, Zsite, ZSITE_STATE_VERIFY
from model.cid import CID_BOOK

class ZsiteBook(McModel):
    pass

def name_join(name_list):
    return ';'.join(i.replace(";","-") for i in name_list)

def name_split(name_list):
    return name_list.split(";")

def zsite_book_new(
    name, 
    douban_id,
    doubna_pic_id,
    author_list, tranlator_list, pages, publisher, isbn10, isbn13, price,
    author_intro, txt,
):
    zsite = zsite_new(name, CID_BOOK)

    book = ZsiteBook.get_or_create(id=zsite.id)
    book.author = name_join(author_list)
    book.tranlator = name_join(tranlator_list) 





if __name__ == '__main__':
    for j, i in enumerate(Zsite.where(cid=CID_COM)):
        print i.name, j
