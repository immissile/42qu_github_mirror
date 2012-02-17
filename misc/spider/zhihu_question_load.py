#coding:utf-8

import _env
from hashlib import md5
from yajl import loads
from glob import glob
from zkit.bot_txt import txt_wrap_by, txt_wrap_by_all
from zkit.htm2txt import unescape, htm2txt
from os.path import exists

def parse_content(txt):
    #id = txt_wrap_by('<a href="/question/', '/log" class="xrv">', txt)
    #t = unescape(txt_wrap_by('<title>', ' - 知乎</title>', txt))
    tlist = txt_wrap_by_all('<div class="xmrw">', '</div>', txt)
    
    r = [htm2txt(i) for i in tlist if i.strip()]

    #for pos, i in enumerate(r[:3]):
    #    print pos, len(i), i
    #    print "\n"
    return r


def zhihu_to_dump():
    with open('/home/zuroc/zpage/misc/spider/zhihu_question_to_dump.json') as zhihu_question_dump:
        for line in zhihu_question_dump:
            line = loads(line)
            key = line[1]
            filename = md5(key).hexdigest()
            #print filename
            path = '/tmp/www.zhihu.com/%s'%filename
            if exists(path):
                yield line_parser(path, line)
            else:
                yield line[-2], line[2], line[-1]

def line_parser(path, line):
    if exists(path):
        with open(path) as f:
            t = f.read()
            if '<h3>邀请别人回答问题</h3>' in t:
                s = parse_content(t)
                return line[-2], line[2], s



if __name__ == '__main__':
    pass


    for i in zhihu_to_dump():
        print i[0], i[1]



