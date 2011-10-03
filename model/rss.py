#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel
from zkit.google.greader import Reader
import json
import sys
from zkit.htm2txt import htm2txt, unescape
from config import GREADER_USERNAME, GREADER_PASSWORD
import traceback


RSS_UNCHECK = 0
RSS_RM = 1
RSS_PRE_PO = 2
RSS_RT_PO = 3
RSS_POED = 4

STATE_RSS_NEW = 5
STATE_RSS_EMAILD = 6
STATE_RSS_REJECT = 7
STATE_RSS_OK = 8

STATE2CN = {
        STATE_RSS_OK:'通过',
        STATE_RSS_NEW:'新建',
        STATE_RSS_EMAILD:'已经联系',
        STATE_RSS_REJECT:'已经被拒绝'
        }

class Rss(McModel):
    pass

class RssPo(McModel):
    pass

class RssPoId(McModel):
    pass

class RssUpdate(McModel):
    pass

def rss_po_id(rss_po_id, po_id):
    RssPoId.raw_sql('insert into rss_po_id (id, po_id, state) values (%s, %s, 0)', rss_po_id, po_id)

def rss_po_total(state):
    return RssPo.where(state=state).count()

def rss_new(user_id, url, name=None, link=None, gid=0, auto=0):
    rss = Rss.get_or_create(url=url)
    rss.user_id = user_id
    rss.gid = gid
    if name:
        rss.name = name
    if link:
        rss.link = link
    rss.auto = int(bool(auto))
    rss.save()
    return rss

def rss_update_new(id, state):
    rss = RssUpdate.get_or_create(id=id)
    rss.state = state
    rss.save()
    return rss


def rss_total_gid(gid):
    return Rss.where(gid=gid).count()

def get_rss_by_gid(gid, limit=1, offset=10):
    rss = Rss.raw_sql('select id,user_id,url,gid,name,link from rss where gid = %s order by id desc limit %s offset %s', gid, limit, offset).fetchall()
    return rss

def rss_po_list_by_state(state, limit=1, offset=10):
    p = RssPo.raw_sql('select id,link,user_id,title,txt,pic_list,rss_id from rss_po where state = %s order by id desc limit %s offset %s', state, limit, offset).fetchall()
    return p


def unread_update(greader=None):
    if greader is None:
        greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)

    feeds = greader.unread_feed()

    for feed in feeds:
        try:
            unread_feed_update(greader, feed)
        except:
            traceback.print_exc()
            continue

    greader.mark_as_read()

def unread_feed_update(greader, feed):
    rs = Rss.raw_sql('select id,user_id from rss where url = %s', feed[5:]).fetchone()
    if rs:
        id, user_id = rs

        res = greader.unread(feed)
        rss_feed_update(res, id , user_id)


def rss_feed_update(res, id, user_id, limit=None):
    from zkit.rss.txttidy import txttidy
    from tidylib import  tidy_fragment


    rss = Rss.mc_get(id)
    for count , i in enumerate(res):
        if limit:
            if count > limit:
                break

        link = i['alternate'][0]['href']
        title = i['title']
        rss_uid = i.get('id') or 1
        snippet = i.get('summary') or i.get('content') or None

        if snippet:
            htm = snippet['content']

            if htm:
                htm = txttidy(htm)
                htm = tidy_fragment(htm,{"indent": 0})[0]

                txt, pic_list = htm2txt(htm)

                pic_list = json.dumps(pic_list)
                if txt:
                    title = unescape(title)
                    if rss.auto:
                        state = RSS_PRE_PO
                    else:
                        state = RSS_UNCHECK
                    RssPo.raw_sql(
'insert into rss_po (user_id,rss_id,rss_uid,title,txt,link,pic_list,state) values (%s,%s,%s,%s,%s,%s,%s,%s) on duplicate key update title=%s , txt=%s , pic_list=%s',
user_id, id, rss_uid, title, txt, link, pic_list, state, title, txt, pic_list
                    )


def rss_subscribe(greader=None):
    from zkit.google.findrss import get_rss_link_title_by_url

    rss_list = []

    for i in Rss.where(gid=0):

        url = i.url.strip()

        if not all((i.link, i.url, i.name)):
            rss, link, name = get_rss_link_title_by_url(url)

            if rss:
                i.url = rss

            if link:
                i.link = link

                if not name:
                    name = link.split('://', 1)[-1]

            if name:
                i.name = name

            i.save()

        rss_list.append(i)

    if rss_list:
        if greader is None:
            greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)

        for i in rss_list:
            greader.subscribe(i.url)
            i.gid = 1
            i.save()
            #print i.url
            feed = 'feed/%s'%i.url
            rss_feed_update(greader.feed(feed), i.id, i.user_id, 256)
            greader.mark_as_read(feed)


    for i in Rss.where('gid<0'):
        if greader is None:
            greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
        greader.unsubscribe('feed/'+i.url)
        #print "unsubscribe",i.url
        i.delete()


if __name__ == '__main__':
    #rss_subscribe()
    # from collections import defaultdict
    # user_id = defaultdict()
    # for i in RssPo.where():
    #     pass

    #greader = Reader(GREADER_USERNAME, GREADER_PASSWORD)
    #greader.empty_subscription_list()
    pass
    #RssPo.where().delete()
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
    from tidylib import  tidy_fragment
    from zkit.rss.txttidy import txttidy
    htm = u"""
<p>将视线从热点频出的消费电子产品市场移开，投向企业级市场，我们可以明显地感受到这样一种趋势——云端的应用和服务开始大量涌现，云的部署开始走向成熟。由于免去了自建平台的负担，中小企业成为了应用云端服务的主力军。那么，中小企业的云端应用的局面如何，又有什么代表性的服务呢？请看下面这张信息图。</p><p><a href="http://www.36kr.com/p/50516.html/cloud" rel="attachment wp-att-50552 external nofollow"><img class="aligncenter size-full wp-image-50552" title="cloud" src="http://img02.36krcnd.com/wp-content/uploads/2011/10/cloud.gif" alt="" width="1000" height="2204" /></a></p><p><strong>信息小结</strong></p><ul><li>据估计，整个世界的云计算市场规模在80亿美元左右。美国市场的地位举足轻重，比重高达40%，约32亿美元。</li><li>流行的云应用包含以下种类：在线客户自定义规划、数据存储与备份、人力资源软件、在线支付程序、财会软件、文档上传与管理、营销软件</li><li>中小企业选择云端服务的理由：可承受的价格(相比自建企业的IT服务)，便捷的资源访问(中小企业普遍具备访问互联网的能力)，快速部署与易用性(多数云端服务都提供免费试用)</li><li>十大云端推荐应用</li><ol><li><strong><a href="http://www.freshbooks.com/" rel="external nofollow">FreshBooks</a></strong>   类型：帐务管理  费用：收费，提供免费试用</li><li><strong><a href="http://www.constantcontact.com/" rel="external nofollow">Constant Contact</a></strong>   类型：客户关系管理  费用：收费，提供免费试用</li><li><strong><a href="http://www.picnik.com/" rel="external nofollow">Picnik</a></strong>   类型：照片分享与编辑  费用：免费</li><li><strong><a href="http://batchblue.com/" rel="external nofollow">Batchbook</a></strong>   类型：客户关系管理 费用：收费，提供免费试用</li><li><strong><a href="http://www.crashplan.com/" rel="external nofollow">CrashPlan</a></strong>   类型：数据备份  费用：免费，高级服务收费</li><li><strong><a href="http://doodle.com/" rel="external nofollow">Doodle</a></strong>   类型：日程安排与会议规划  费用：免费</li><li><strong><a href="http://www.dropbox.com/" rel="external nofollow">Dropbox</a></strong>   类型：文件分享  费用：免费，高级服务收费</li><li><strong><a href="http://www.carboniteaddon.com/" rel="external nofollow">Carbonite</a></strong> 类型：数据备份 费用：收费，提供免费试用</li><li><strong><a href="http://outright.com/" rel="external nofollow">outright</a></strong> 类型：财务管理 费用：收费，提供免费试用</li><li><strong><a href="http://quickbooks.intuit.com/" rel="external nofollow">QuickBooks</a></strong> 类型：帐务管理 费用：收费，提供免费试用</li></ol></ul><p>pic via <a href="http://www.formstack.com/assets/images/infographics/journey-to-the-cloud.gif" rel="external nofollow">Formstack</a></p><p>除非注明，本站文章均为原创或编译，转载请注明： 文章来自<a rel="bookmark" title="【信息图】中小企业的云端之路" href="http://www.36kr.com/p/50516.html">36氪</a></p><img width='1' height='1' src='http://feed.36kr.com/c/33346/f/566026/s/1903a03b/mf.gif' border='0'/><br/><br/><a href="http://da.feedsportal.com/r/114252605090/u/351/f/566026/c/33346/s/1903a03b/a2.htm"><img src="http://da.feedsportal.com/r/114252605090/u/351/f/566026/c/33346/s/1903a03b/a2.img" border="0"/></a>
i在
"""
    print "\n"*11
    htm = txttidy(htm)
    htm = tidy_fragment(htm,{"indent": 0})[0]
    print htm

