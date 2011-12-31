#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
import urllib2
from urllib2 import urlopen
from model._db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from model.po import po_new, STATE_RM
from model.po_event import po_event_pic_new , EVENT_CID, po_event_feedback_new
from model.event import Event, event_init2to_review
from model.state import STATE_RM, STATE_SECRET, STATE_ACTIVE
from model.cid import CID_EVENT, CID_EVENT_FEEDBACK, CID_NOTICE_EVENT_JOINER_FEEDBACK, CID_NOTICE_EVENT_ORGANIZER_SUMMARY
from model.event import Event, EVENT_STATE_INIT, EVENT_STATE_REJECT, EVENT_STATE_TO_REVIEW, EVENT_STATE_NOW, EVENT_JOIN_STATE_END, EVENT_JOIN_STATE_YES, EVENT_JOIN_STATE_FEEDBACK_GOOD, EVENT_JOIN_STATE_FEEDBACK_NORMAL, event_new_if_can_change, EventJoiner, event_joiner_user_id_list, event_joiner_get, event_joiner_state, last_event_by_zsite_id, event_new
from model.po_event import po_event_pic_new , EVENT_CID, po_event_feedback_new
from model.days import today_ymd_int, ymd2minute, minute2ymd, ONE_DAY_MINUTE
from urllib import urlencode
from zkit.pic import picopen
from json import loads
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from xml.sax.saxutils import unescape
from zkit.htm2txt import htm2txt
from zkit.spider import Rolling, Fetch, NoCacheFetch, GCrawler
from time import sleep
from os.path import exists
import os.path
from zkit.earth import PID2NAME
import re

event_cid = 9 #其他


class EventImport(Model):
    pass

DOUBAN_SITE_LIST = (
        # url , user_id , zsite_id
        (' http://site.douban.com/widget/events/117123/',10074584,10199666),#单向街      
        (' http://site.douban.com/widget/events/1409398/',10000065,10091192),#Python     
        (' http://site.douban.com/widget/events/326387/',10018609,10133826),#真人图书馆  
        (' http://site.douban.com/widget/events/1226483/',10010448,10126347),#科学松鼠会 
        (' http://site.douban.com/widget/events/4134513/',10018576,10200247),#豆瓣公开课 
        (' http://site.douban.com/widget/events/3954604/',10019039,10200245), #草地音乐 
)




TIME_BY_DOUBAN = re.compile('(\d+)')

def time_by_douban(s):
    return datetime(*map(int, TIME_BY_DOUBAN.findall(s)))
 
def save_event( phone, address, begin_time, end_time, pic, title, intro, douban_event_id):

    city = address[0]
    place = address[1]
    address = address[2]

    begin_time = time_by_douban(begin_time)
    end_time = time_by_douban(end_time)


    pid = 1
    for k, v in PID2NAME.items():
        if v == place:
            pid = k
            break

    city_pid = 1
    for k, v in PID2NAME.items():
        if v == city:
            city_pid = k
            break


    #TODO datetime -> int model/days.py
    begin = ymd2minute(begin_time)+begin_time_hour*60+begin_time_minute
    end = ymd2minute(end_time)+end_time_hour*60+end_time_minute

    id = 0
    limit_up = 42
    limit_down = 0
    transport = ''
    price = 0
    event = event_new(
        self.user_id,
        event_cid,
        city_pid,
        pid,
        address,
        transport,
        begin,
        end,
        int(100*price),
        limit_up,
        limit_down,
        phone,
        0,
        id
    )

    id = event.id

    po = po_new(CID_EVENT, self.user_id, '', STATE_SECRET , id=id, zsite_id=self.zsite_id)
    po.name_ = title
    po.txt_set(htm2txt(intro)[0])
    po.save()

    event_init2to_review(po.id)
    EventImport(id, int(event_id)).save()

    return event

def save_pic(pic, pic_url, event):
    pic = picopen(pic)
    if not pic:
        return
    else:
        pic_id = po_event_pic_new(event.user_id, pic)
        event.pic_id = pic_id
        event.save()

class ParseEventIndex(object):
    def __init__(self, user_id , zsite_id):
        self.zsite_id = zsite_id
        self.user_id = user_id

    def __call__(self, html, url):
        html = txt_wrap_by('<ul class="list-m">', '</ul>', html)
        items = txt_wrap_by_all('<li class="item">', '</div>', html)

        links = []
        for item in items:
            link = txt_wrap_by('href="', '"', item)

            id = txt_wrap_by('http://www.douban.com/event/', '/', link)
            id = int(id)

            event = EventImport.get(id)
            if not event:
                yield self.parse_event_page, link ,  id
    
    def parse_event_page(self, page, url, douban_event_id):
        title = txt_wrap_by('h1>', '</h1>', page)
        pic_url = txt_wrap_by('href="', '"', txt_wrap_by('class="album_photo"', '>', page))
        begin_time = txt_wrap_by('ail">', '<', txt_wrap_by('开始时间', '/div', page))
        end_time = txt_wrap_by('ail">', '<', txt_wrap_by('结束时间', '/div', page))
        address = unicode(txt_wrap_by('span>', '<', txt_wrap_by('地点', 'br/>', txt_wrap_by('class="obmo">', '</div', page)))).split(' ')
        typ = txt_wrap_by('类型: </span>', '<br/', page)
        intro = txt_wrap_by('play:none">', '<a href="javasc', page)
        phone = txt_wrap_by('电话', '<br/', intro)
        if phone:
            phone = phone.replace('：', '').replace(':', '')

        event = save_event(phone, address, begin_time, end_time, pic_url, title, intro, douban_event_id)

        yield save_pic, pic_url,  event
            # pic = page_fetch(pic)
                

def main():
    url_list = []
    for url, user_id, zsite_id in DOUBAN_SITE_LIST:
        url_list(ParseEventIndex(user_id, zsite_id), url)

    self.url, self.user_id, self.zsite_id = url, user_id, zsite_id
    headers = {
        'Cookie':'bid=i9gsK/lU40A'
    }
    self.fetcher = NoCacheFetch(20, headers=headers)
    self.spider = Rolling( self.fetcher, url_list )
    spider_runner = GCrawler(self.spider, workers_count=10)
    spider_runner.start()

if __name__ == '__main__':
    main()
