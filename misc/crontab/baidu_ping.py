#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
import xmlrpclib
from model.po import Po
from zweb.orm import ormiter
import time
from model.state import STATE_ACTIVE
from model.cid import CID_NOTE
from model.zsite import Zsite
import logging

logging.basicConfig(filename='seo_ping.log',level=logging.INFO,)


"""
    YOUDAO_PING_URL = "http://blog.youdao.com/ping/RPC2" 
    GOOGLE_PING_URL = "http://blogsearch.google.com/ping/RPC2"
    OMATIC_PING_URL = "http://rpc.pingomatic.com"
    
http://www.baidu.com/search/blogsearch_help.html

发送给博客搜索Ping服务的XML-RPC客户请求需要包含如下元素：
RPC端点： http://ping.baidu.com/ping/RPC2
调用方法名： weblogUpdates.extendedPing
参数： (应按照如下所列的相同顺序传送)
博客名称
博客首页地址
新发文章地址
博客rss地址
"""
PING_URL=["http://ping.baidu.com/ping/RPC2",
          #"http://blog.youdao.com/ping/RPC2",
          "http://blogsearch.google.com/ping/RPC2",
          #"http://rpc.pingomatic.com",
         ]
BAIDU_PING_URL = 'http://ping.baidu.com/ping/RPC2'
def ping_po():
    ten_mins = int(time.time()) - 60*10
    for po in ormiter(Po, 'cid=%s and state=%s and create_time>%s'%\
                      (CID_NOTE, STATE_ACTIVE, ten_mins)):
        ping_all(po)


from model.zsite_url import url_by_id

def ping_all(po):
    zsite = Zsite.get(po.user_id)
    blog_name = zsite.name
    url = url_by_id(po.user_id)
    blog_index = 'http://%s.42qu.com/'%(url or po.user_id)
    po_link = '%s%s'%(blog_index, po.id)
    rss_link = blog_index+'rss'
    now = time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
    logging.info("%s %s\n%s %s %s %s"%(now, po.name, blog_name, blog_index, po_link, rss_link))
    print po.name
    
    for ping_url in PING_URL:
        server = xmlrpclib.ServerProxy(ping_url)
        response = server.weblogUpdates.extendedPing(blog_name, blog_index, po_link, rss_link)
        print response

if __name__ == '__main__':
    #ping_po()
    #po = Po.get(10037317)
    #ping_all(po)
    po_id_list = Po.where("cid=62 and id<10046800").order_by("id desc")
    for po in po_id_list:
        ping_all(po)
