#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
import _env
from zkit.bot_txt import txt_wrap_by_all
from zkit.htm2txt import htm2txt
from json import loads,dumps
import os

SOURCE_ROOT = './'
SOURCE_DIR = 'zhihu/'

question_set = set()
question_set_fetched = set()

def main():
    for root,dirs,files in os.walk(SOURCE_ROOT):
        for i in files:
            try:
                find_next(os.path.join(root,i))
            except:
                print 'error ',i
    find_not_fetched()

def find_next(page_file):
    global question_set_fetched,question_set
    with open(page_file) as page:
        link = set(txt_wrap_by_all('<a class="xu" name="rlq" id="rlq-','"',  page.read()))
        question_set|=link

def find_not_fetched():
    global question_set_fetched,question_set
    with open(SOURCE_ROOT+'zhihu.txt') as page:
        for line in page:
            try:
                question_set_fetched|=set(line.strip().split()[1])
            except:
                continue
    with open(SOURCE_ROOT+'zhihu.txt','a') as zhihu:
        zhihu.writelines(['0\t'+x+"\tmissed\n" for x in  question_set-question_set_fetched])

if __name__ == '__main__':
    main()
