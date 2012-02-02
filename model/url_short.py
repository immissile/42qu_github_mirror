#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from _db import  Model
from config import SHORT_DOMAIN
from zkit.num2code import num_decode, num_encode
from zkit.img_filter import img_filter
from txt2htm import RE_LINK


SHORT_LINK = 'http://%s'%SHORT_DOMAIN
class UrlShort(Model):
    pass

def replace_link(match, user_id):
    from po_video import  video_filter
    gs = match.groups()
    g = gs[0]
    if not ( video_filter(g)[0] or img_filter(g) or g.startswith(SHORT_LINK) ):
        g = url_short(g, user_id)
    return g

def id2url(id):
    if id:
        s_url_id = num_encode(id)
        link = '%s/%s' % (SHORT_LINK, s_url_id)
        return link

def url_short_id(url, user_id=0):
    url = url.strip()
    if url:
        url_short = UrlShort.get_or_create(value=url, user_id=user_id)
        url_short.save()
        return url_short.id

def url_short(url, user_id=0):
    id = url_short_id(url,user_id)
    return id2url(id)

def url_short_by_key(key):
    id = num_decode(key)
    return url_short_by_id(id)

def url_short_by_id(id):
    url = UrlShort.get(id)
    if url:
        return url.value
    return ''

def url_short_txt(s, user_id=0):

    if type(s) is unicode:
        s = str(s)
    s = RE_LINK.sub(lambda match:replace_link(match, user_id), s)
    return s

if __name__ == '__main__':
#for i in range(199):
#    print url_short("http://google"+str(i))
    print url_short_by_key('mJbC')

#print url_short_by_id('3T')
    #print url_short_txt('sfsdfsdf http://g.cn/df.png http://google.com https://mail.google.com/mail/u/0/#inbox/134ec4da6de5b5a7 https://mail.google.com/mail/u/0/#inbox')
    #print url_short("http://baidu.com")
    #id = url_short_id('http://google.com/ncr')
    #print url_short_by_id(id)
    print url_short_by_key('MK')
    print url_short_txt("""
英文的学术叫法叫做 re-visit policy ( http://en.wikipedia.org/wiki/Web_crawler )
简单的说, 就是通过历史的抓取页面更新, 预测下一次的抓取更新的时间
http://oak.cs.ucla.edu/~cho/research/crawl.html 页面上有一个论文汇总 , 可以下载这些论文
Ka Cheung Sia, Junghoo Cho "Efficient Monitoring Algorithm for Fast News Alert." Technical Report, UCLA Computer Science Department, June 2005.
英文的学术叫法叫做 re-visit policy ( [[http://42qu.us/mJbJ]] )
""")
