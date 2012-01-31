#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bot_txt import txt_map
from upyun import upyun_rsspic, upyun_fetch_pic
from htm2txt import htm2txt

def txt_img_fetch(txt):
    return txt_map(r'图:', r'::图', txt, fetch_pic)

def fetch_pic(url):
    link = False
    url = url.replace('图:','').replace('::图','')
    if '[[' in url:
        link = True
        url = url.replace('[[','')

    if '.feedsky.com/' in url or '1.42qu.us' in url:
        result = ''
    else:
        result = upyun_fetch_pic(url)
        if result:
            result = '图:%s '%result
        else:
            result = ''
    if link:
        result+='[['
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
    print txt_img_fetch(htm2txt(a))
