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
            attribute = data['db:attribute']

            result = {}
            for i in attribute:
                key = i['@name']
                value = i['$t']
                if key == 'author':
                    continue

                if key == 'isbn13':
                    key = 'isbn'

                if key == 'translator':
                    if key not in result:
                        result[key] = []
                    result[key].append(value)
                else:
                    result[key] = value

            link = data['link']

            for i in link:
                key = i['@rel']
                value = i['@href']
                result[key] = value

            name = result['title']
            pic_id = result['image'].rsplit('s', 1)[-1][:-4]
            print name.encode('utf-8', 'ignore'), pic_id

            #{u'publisher': u'\u82b1\u57ce\u51fa\u7248\u793e', 'isbn': u'9787536045958', u'isbn10': u'7536045956', u'pubdate': u'2005-9', u'title': u'\u5341\u5e74\u706f', u'price': u'25.0', u'binding': u'\u5e73\u88c5', u'pages': u'309'}


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
