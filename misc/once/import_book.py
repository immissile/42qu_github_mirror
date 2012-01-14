#coding:utf-8

import _env

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from zkit.retry import urlfetch
from time import sleep
from json import loads

def name_join(name_list):
    return ';'.join(
        i.strip().replace(';', '-') for i in name_list
    )

url = 'http://api.douban.com/book/subject/isbn/%s?apikey=00d9bb33af90bf5c028d319b0eb23e14&alt=json'
with open('bookisbn.txt') as bookisbn:
    for line in bookisbn:
        line = line.strip()
        data = urlfetch(url%line)
        data = loads(data)
        name_list = []
        for item in data['author']:
            name_list= [
                item[u'name'][u'$t'].encode("utf-8")
            ]
        
        author = name_join(name_list)
        
        data = {}
        attribute = data['db:attribute']
        for i in attribute:
            key = t[i]['@name']
            value = t[i]['$t']
            if key=='author':
                continue

            if key=="isbn13":
                key='isbn'
    
            if key=='translator':
                if not data[key]:
                    data[key]=[]
                data[key].push(value)
            else:
                data[key]=value
            
            

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
