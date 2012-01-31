#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bot_txt import txt_map
from upyun import upyun_rsspic, upyun_fetch_pic

def txt_img_fetch(txt):
    return txt_map('图:', ' ', txt, lambda x:fetch_pic(x[4:]))

def fetch_pic(url):
    if '.feedsky.com/' in url:
        result = ''
    else:
        result = upyun_fetch_pic(url)
        result = '图:%s '%result

    return result

if __name__ == '__main__':
    a = '''
    图:http://p4.42qu.us/721/854/168790.jpg 
    如果
    **某一天**
    ，
    你身上多了一个“恢复出厂设置”按钮，一按身体和记忆一切归为出生时。 你会去按它吗？
    '''

    print txt_img_fetch(a)
