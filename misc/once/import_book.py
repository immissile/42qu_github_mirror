#coding:utf-8

import _env

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from zkit.retry import urlfetch
from time import sleep
from json import loads
from model.zsite_book import isbn_by_str

def name_join(name_list):
    return ';'.join(
        i.strip().replace(';', '-') for i in name_list
    )

URL = 'http://api.douban.com/book/subject/isbn/%s?apikey=00d9bb33af90bf5c028d319b0eb23e14&alt=json'

def import_book_by_isbn(isbn, from_id=0):
    pass

def import_by_file(filename, from_id=0):
    with open(filename) as bookisbn:
        for line in bookisbn:
            line = line.strip()
            isbn = isbn_by_str(line)
            if not isbn:
                print line
                continue
            link = URL%isbn
            print link
            data = urlfetch(link)
            data = loads(data)
            name_list = []
            if 'author' in data:
                for item in data['author']:
                    name_list.append( 
                        item[u'name'][u'$t'].encode('utf-8')
                    )

            author = name_join(name_list)
            print data
            attribute = data['db:attribute']
            for i in attribute:
                key = i['@name']
                value = i['$t']
                if key == 'author':
                    continue

                if key == 'isbn13':
                    key = 'isbn'

                if key == 'translator':
                    if key not in data:
                        data[key] = []
                    data[key].append(value)
                else:
                    data[key] = value


            print data
            sleep(1)

#name =  self.get_argument('title', '无题') 
#pic_id = self.get_argument('pic_id', 0)
#author = self.get_argument('author','')
#translator = self.get_argument('translator','')
#pages = self.get_argument('pages','')
#publisher = self.get_argument('publisher','')

#isbn = self.get_argument('isbn',0)
#rating = self.get_argument('rating','')
#rating_num = self.get_argument('rating_num','')

#author_intro = self.get_argument('author-intro','')
#txt = self.get_argument('txt','')

#id = zsite_book_new(
#    name, douban_id, pic_id,
#    author, translator, pages,  
#    publisher, isbn,
#    int(float(rating)*100), rating_num,
#    author_intro, txt
#)

import_by_file('book_all.txt')
import_by_file('book_zf.txt')
