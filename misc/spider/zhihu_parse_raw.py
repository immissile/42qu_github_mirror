#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from zkit.htm2txt import htm2txt
import glob

HTML_LIST = glob.glob('/mnt/zdata/zhihu_full/*.html')


def html_yield():
    for i in HTML_LIST:
        with open(i) as html:
            yield html.read()


def page_parse(html):
    title = txt_wrap_by('<title>', '- 知乎', html)
    tags = txt_wrap_by_all('data-tip="t$b$', '"', html)
    for i in tags:
        print i,
    print title
    print ''

#    #reply_raw_list = txt_wrap_by_all('<div class="xmo">','class="xnq xml xnh">',html)
#    #replies = [ htm2txt(x)[0] for x in reply_raw_list ]
#
#    #js = '{}'
#    #js = '["current_question",' +txt_wrap_by("(['current_question', ",');',html)
#    #a = loads(js)
#
#    answer_list=[]
#
#    #question_info={}
#    #question_info['answer'] = answer_list
#    #question_info['l'] = [ x[0] for x in a[1][ ]
#    #question_info['title'] = title
#    #question_info['body'] = htm2txt(txt_wrap_by('<div class="xvrw">','<a href="javascript',html))[0]
#    #replies_line = zip(a[1][12],replies)
#
#    count = txt_wrap_by('h3 style="margin: 0 0 5px;">','个答案',html)
#
#    question_info={}
#    question_info['answer'] = answer_list
#    question_info['tags'] = tags
#    question_info['title'] = title
#    question_info['body'] = ''
#    question_info['count'] =  count
#    #for x in replies_line:
#    #    try:
#    #        new_ans={}
#    #        new_ans['name'] = x[0][2][0]
#    #        new_ans['answer'] = x[1]
#    #        new_ans['id'] = x[0][2][1]
#    #        new_ans['signature'] = x[0][3]
#    #        new_ans['votes'] = x[0][4]
#    #        answer_list.append(new_ans)
#    #    except:
#    #        continue
#
#    if count > 0:
#        FETCH_LIST.append((htm_file,int(count)))
#    #out_file.write(dumps(question_info)+'\n')
#
def main():
    for i in html_yield():
        page_parse(i)
#    for root,dirs,files in os.walk(SOURCE_ROOT):
#        for i in files:
#            page_parse(os.path.join(root,i))
#    out_file.close()
#    FETCH_LIST.sort(key=lambda x:x[1],reverse=True)
#    for id,count in FETCH_LIST:
#        print id,count
#
if __name__ == '__main__':
    main()
