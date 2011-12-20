#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _db
from _db import Model, McModel, McCache, McLimitM, McNum, McCacheA, McCacheM, McCacheA, McLimitA
from model.zsite import zsite_new, ZSITE_STATE_ACTIVE, Zsite, ZSITE_STATE_VERIFY
from model.cid import CID_BOOK
from txt import txt_new



# DROP TABLE IF EXISTS `zpage`.`zsite_book_lib`;
# CREATE TABLE  `zpage`.`zsite_book_lib` (
#   `id` int(10) unsigned NOT NULL auto_increment,
#   `book_id` int(10) unsigned NOT NULL default '0',
#   `owner_id` int(10) unsigned NOT NULL default '0',
#   `state` int(10) unsigned NOT NULL default '0',
#   `pid` int(10) unsigned NOT NULL default '0',
#   `from_id` int(10) unsigned NOT NULL default '0',
#   PRIMARY KEY  (`id`),
#   KEY `Index_3` (`book_id`,`state`),
#   KEY `Index_2` USING BTREE (`owner_id`)
# ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=binary;
# 
# DROP TABLE IF EXISTS `zpage`.`zsite_book_browse`;
# CREATE TABLE `zpage`.`zsite_book_browse` (
#   `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#   `expire` INTEGER UNSIGNED NOT NULL,
#   `begin_time` INTEGER UNSIGNED NOT NULL,
#   PRIMARY KEY (`id`),
# )
# 
# DROP TABLE IF EXISTS `zpage`.`zsite_book`;
# CREATE TABLE  `zpage`.`zsite_book` (
#   `id` int(10) unsigned NOT NULL auto_increment,
#   `douban_id` int(10) unsigned NOT NULL default '0',
#   `isbn` bigint(20) unsigned NOT NULL default '0',
#   `pages` int(10) unsigned NOT NULL,
#   `author` varbinary(512) NOT NULL,
#   `translator` varbinary(512) NOT NULL,
#   `publisher` varbinary(128) NOT NULL,
#   `author_intro` blob NOT NULL,
#   `douban_pic_id` int(10) unsigned NOT NULL default '0',
#   `rating` smallint(5) unsigned NOT NULL default '0',
#   `rating_num` int(10) unsigned NOT NULL default '0',
#   PRIMARY KEY  (`id`),
#   KEY `Index_2` USING BTREE (`douban_id`),
#   KEY `Index_3` USING BTREE (`isbn`)
# ) ENGINE=MyISAM AUTO_INCREMENT=2389 DEFAULT CHARSET=binary;
# 
# DROP TABLE IF EXISTS `zpage`.`zsite_book_browse_history`;
# CREATE TABLE `zpage`.`zsite_book_browse_history` (
#   `id` INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
#   `book_lib_id` INTEGER UNSIGNED NOT NULL,
#   `begin_time` INTEGER UNSIGNED NOT NULL,
#   `end_time` INTEGER UNSIGNED NOT NULL,
#   `user_id` INTEGER UNSIGNED NOT NULL,
#   PRIMARY KEY (`id`),
#   INDEX `Index_2`(`user_id`),
#   INDEX `Index_3`(`book_lib_id`)
# )
# ENGINE = MyISAM;

mc_zsite_book_id_by_isbn = McCache('ZsiteBookIdByIsbn:%s')

ZSITE_BOOK_LIB_STATE_EXIST  = 10
ZSITE_BOOK_LIB_STATE_BROWSE = 20
ZSITE_BOOK_LIB_STATE_LOST = 30

ZSITE_BOOK_LIB_STATE2CN = {
    ZSITE_BOOK_LIB_STATE_EXIST  : "在库" ,
    ZSITE_BOOK_LIB_STATE_BROWSE : "借出" , 
    ZSITE_BOOK_LIB_STATE_LOST   : "丢失" ,
}

class ZsiteBookBrowseHistory(Model):
    pass

class ZsiteBookBrowse(Model):
    pass

class ZsiteBookLib(McModel):
    @property
    def is_exist(self):
        return self.state == ZSITE_BOOK_LIB_STATE_EXIST


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
    l = list(ZsiteBookLib.where().order_by('book_id desc'))
    Zsite.mc_bind(l, 'zsite', 'book_id')
    return l

def zsite_book_by_lib(book_id):
    l = ZsiteBookLib.where(book_id=book_id)
    return list(l)

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
