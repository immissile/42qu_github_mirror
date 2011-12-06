#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from zkit.htm2txt import htm2txt
from json import loads,dumps
import os

PARSED_FILENAME = 'out.js'
SOURCE_ROOT = 'misc/once/zhihu/'
out_file = open(PARSED_FILENAME,'w')

def crawl_files():
    for root,dirs,files in os.walk(SOURCE_ROOT):
        for i in files:
            print (os.path.join(root,i))


def page_parse(htm_file):

    html = open(htm_file).read()
    title = txt_wrap_by('<title>','- 知乎',html)

    reply_raw_list = txt_wrap_by_all('<div class="xmo">','class="xnq xml xnh">',html)

    replies = [ htm2txt(x)[0] for x in reply_raw_list ]

    js = '["current_question",' +txt_wrap_by("DZMT.push(['current_question', ",');',html)
    a = loads(js)

    answer_list=[]

    question_info={}
    question_info['answer'] = answer_list
    question_info['tags'] = [ x[0] for x in a[1][3] ]
    question_info['title'] = title
    question_info['body'] = htm2txt(txt_wrap_by('<div class="xvrw">','<a href="javascript',html))[0]
    replies_line = zip(a[1][12],replies)

    for x in replies_line:
        try:
            new_ans={}
            new_ans['name'] = x[0][2][0]
            new_ans['answer'] = x[1]
            new_ans['id'] = x[0][2][1]
            new_ans['signature'] = x[0][3]
            new_ans['votes'] = x[0][4]
            answer_list.append(new_ans)
        except:
            continue
    out_file.write(dumps(question_info))

if __name__ == '__main__':
    #page_parse("test.html")
    #out_file.close()
    crawl_files()
