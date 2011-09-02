#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
import xmlrpclib
from model.po import Po
from zweb.orm import ormiter
from model.state import STATE_ACTIVE
from model.cid import CID_NOTE
from zkit.single_process import single_process
from model.kv_misc import kv_int_call, KV_SEO_PING


'''
YOUDAO_PING_URL = 'http://blog.youdao.com/ping/RPC2'
GOOGLE_PING_URL = 'http://blogsearch.google.com/ping/RPC2'
OMATIC_PING_URL = 'http://rpc.pingomatic.com'
BAIDU_PING_URL = 'http://ping.baidu.com/ping/RPC2'

http://www.baidu.com/search/blogsearch_help.html

发送给博客搜索Ping服务的XML-RPC客户请求需要包含如下元素:
RPC端点: http://ping.baidu.com/ping/RPC2
调用方法名: weblogUpdates.extendedPing
参数: (应按照如下所列的相同顺序传送)
博客名称
博客首页地址
新发文章地址
博客rss地址
'''

PING_URL = [
    'http://ping.baidu.com/ping/RPC2',
    #'http://blog.youdao.com/ping/RPC2',
    'http://blogsearch.google.com/ping/RPC2',
    #'http://rpc.pingomatic.com',
]


def ping_po(begin):
    if begin < 10075567:
        begin = 10075567
    po = None
    for po in ormiter(Po, 'id > %s and cid=%s and state=%s' % (begin, CID_NOTE, STATE_ACTIVE)):
        ping_all(po)
    if po:
        return po.id


def ping_all(po):
    zsite = po.user
    blog_name = zsite.name
    blog_index = 'http:%s' % zsite.link
    po_link = '%s/%s' % (blog_index, po.id)
    rss_link = '%s/rss' % blog_index
    #print po.name

    for ping_url in PING_URL:
        server = xmlrpclib.ServerProxy(ping_url)
        response = server.weblogUpdates.extendedPing(blog_name, blog_index, po_link, rss_link)
        #print response

@single_process
def main():
    kv_int_call(KV_SEO_PING, ping_po)

if __name__ == '__main__':
    main()
