#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bot_txt import txt_map
from upyun import upyun_rsspic, upyun_fetch_pic

def txt_img_fetch(txt):
    return txt_map('图:', ' ', txt, fetch_pic)

def fetch_pic(url):
    url = url.decode('utf-8','ignore')[2:]
    if '.feedsky.com/' in url:
        result = ''
    else:
        result = upyun_fetch_pic(url)
        if result:
            result = '图:%s '%result
        else:
            result = ''
    return result

if __name__ == '__main__':
    a = '''
    图:http://tp2.sinaimg.cn/1483383365/50/5610781374/0 
    如果
    **某一天**
    ，
    你身上多了一个“恢复出厂设置”按钮，一按身体和记忆一切归为出生时。 你会去按它吗？
    '''
    print txt_img_fetch(a)
