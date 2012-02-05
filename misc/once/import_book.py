#coding:utf-8

import _env

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from zkit.retry import urlfetch
from time import sleep
from json import loads
from model.zsite_book import isbn_by_str, zsite_book_id_by_isbn, zsite_book_new, zsite_book_by_lib, zsite_book_lib_new

def name_join(name_list):
    return ';'.join(
        i.strip().replace(';', '-') for i in name_list
    )

URL = 'http://api.douban.com/book/subject/isbn/%s?apikey=00d9bb33af90bf5c028d319b0eb23e14&alt=json'

def import_by_file(filename, from_id=0):
    with open(filename) as bookisbn:
        for line in bookisbn:
            line = line.strip()
            isbn = isbn_by_str(line)
            book_id = None
            if isbn:
                book_id = zsite_book_id_by_isbn(isbn)
                if not book_id:
                    link = URL%isbn
                    data = urlfetch(link)
                    if not data:
                        continue

                    data = loads(data)
                    if 'id' not in data:
                        isbn = None

                    if not isbn:
                        continue

                    douban_id = data['id']['$t'].rsplit('/', -1)[-1]
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

                    translator = name_join(
                        result.get('translator', ())
                    )

                    pages = result.get('pages','0')
                    if not pages.isdigit():
                        pages = 0
                    publisher = result.get('publisher', '').encode('utf-8', 'ignore')
                    rating = data['gd:rating']['@average']
                    rating_num = data['gd:rating']['@numRaters']
                    if 'summary' in data:
                        txt = data['summary']['$t']
                    else:
                        txt = ''
                    book_id = zsite_book_new(
                        name.encode('utf-8', 'ignore'),\
                          douban_id,\
                          pic_id,\
                          author,\
                          translator,\
                          int(pages),\
                          publisher,\
                          result['isbn'],\
                          int(float(rating)*100),\
                          rating_num,\
                          result.get('author-intro', ''),\
                          txt.encode('utf-8', 'ignore')
                    )
                    sleep(1)

            if book_id:
                if not zsite_book_by_lib(book_id):
                    zsite_book_lib_new(book_id, 1, from_id)
    
    with open(filename) as bookisbn:
        for line in bookisbn:
            line = line.strip()
            isbn = isbn_by_str(line)
            book_id = None
            if isbn:
                book_id = zsite_book_id_by_isbn(isbn)
            if not book_id:
                print line

 
import_by_file('book_all.txt')
import_by_file('book_zf.txt')
