#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.bot_txt import txt_map
from model.upyun import upyun_fetch_pic
from urlparse import urlparse
from config import UPYUN_DOMAIN

def txt_img_fetch(txt):
    return txt_map(r'图:', '\n', txt+'\n', fetch_pic).rstrip('\n')


def fetch_pic(line):
    url = str(line)[4:-1]
    pos = url.find("[[")
    if pos>0:
        url = url[:pos].strip()

    netloc = urlparse(url)[1]

    if not netloc:
        return ''


    for i in (
        'feedsky.com/',
        'feedburner.com/',
        'wumii.com/',
        '/wp-content/plugins/',
    ):
        if i in url:
            return ''

    if netloc == UPYUN_DOMAIN:
        return line


    result = upyun_fetch_pic(url)
    if result:
        result = '图:%s\n'%result
    else:
        result = line

    return result

if __name__ == '__main__':
    a = '''
    图:[[http:///sdfsdf]]
    <a href="http://tp2.sinaimg.cn/1483383365/50/5610781374/0"><img src='http://tp2.sinaimg.cn/1483383365/50/5610781374/0'/></a>
    如果
    **某一天**
    ，
    你身上多了一个“恢复出厂设置”按钮，一按身体和记忆一切归为出生时。 你会去按它吗？
    '''
    from zkit.htm2txt import htm2txt
    print txt_img_fetch(htm2txt(a))


