#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
import urllib2
from urllib2 import urlopen
from model.event_map import EventImport
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
from time import sleep
from os.path import exists
import os.path
from zkit.earth import PID2NAME
import re

event_cid = 9 #其他


DOUBAN_SITE_LIST = (
        #url,userid,zsiteid
        #('http://site.douban.com/widget/events/117123/',10031395,10133826),
        ('http://site.douban.com/widget/events/117123/',10074584,10199666),#单向街
        ('http://site.douban.com/widget/events/1409398/',10000065,10091192),#Python
        ('http://site.douban.com/widget/events/326387/',10018609,10133826),#真人图书馆
        ('http://site.douban.com/widget/events/1226483/',10010448,10126347),#科学松鼠会
        ('http://site.douban.com/widget/events/4134513/',10018576,10200247),#豆瓣公开课
        ('http://site.douban.com/widget/events/3954604/',10019039,10200245), #草地音乐
        )

def page_fetch(url):
    headers = {
            'Cookie':'bid=i9gsK/lU40A'
            }
    request = urllib2.Request(
            url=url,
            headers=headers
    )
    urlopener = urllib2.build_opener()
    r = urlopener.open(request)
    j = r.read()

    return j

def sync_db(id, event_id):
    EventImport(id, int(event_id)).save()

class DoubanSite(object):
    def __init__(self, url, user_id, zsite_id):
        super(DoubanSite, self).__init__()
        self.url, self.user_id, self.zsite_id = url, user_id, zsite_id
        self.page = page_fetch(self.url)
        self.page = txt_wrap_by('<ul class="list-m">', '</ul>', self.page)
        self.items = txt_wrap_by_all('<li class="item">', '</div>', self.page)

        self.links = []
        for item in self.items:
            self.links.append(txt_wrap_by('href="', '"', item))

        self.handle_link()

    def add_event(self, phone, address, begin_time, end_time, pic, title, intro):

        city = address[0]
        place = address[1]
        address = address[2]

        time_builder = re.compile('(\d+)')
        begin_time_list = time_builder.findall(begin_time)
        end_time_list = time_builder.findall(end_time)

        if len(begin_time_list[2]) < 2:
            begin_time_list[2] = '0'+begin_time_list[2]

        if len(end_time_list[2]) < 2:
            end_time_list[2] = '0'+end_time_list[2]

        if len(begin_time_list[1]) < 2 :
            begin_time_list[1] = '0'+begin_time_list[1]

        if len(end_time_list[1]) < 2 :
            end_time_list[1] = '0'+end_time_list[1]

        begin_time = int(''.join(begin_time_list[:3]))
        end_time = int(''.join(end_time_list[:3]))


        phone = phone
        address = address
        limit_up = 42
        limit_down = 0
        transport = ''
        price = 0

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


        begin_time_hour = int(begin_time_list[3])
        begin_time_minute = int(begin_time_list[4])

        end_time_hour = int(end_time_list[3])
        end_time_minute = int(end_time_list[4])

        pic = page_fetch(pic)
        pic = picopen(pic)
        if not pic:
            raise
        else:
            pic_id = po_event_pic_new(self.user_id, pic)

        begin = ymd2minute(begin_time)+begin_time_hour*60+begin_time_minute
        end = ymd2minute(end_time)+end_time_hour*60+end_time_minute
        id = 0
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
            pic_id,
            id
        )

        id = event.id

        po = po_new(CID_EVENT, self.user_id, '', STATE_SECRET , id=id, zsite_id=self.zsite_id)
        po.name_ = title
        po.txt_set(htm2txt(intro)[0])
        po.save()

        event_init2to_review(po.id)
        return id


    def handle_page(self, page):
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

        return self.add_event(phone, address, begin_time, end_time, pic_url, title, intro)

    def handle_link(self):
        for link in self.links:
            id = txt_wrap_by('http://www.douban.com/event/', '/', link)
            id = int(id)

            event = EventImport.get(id)
            if not event:
                page = page_fetch(link)
                event_id = self.handle_page(page)
                sync_db(id, event_id)

#filename = os.path.join('danxiangjie', id)
#if not exists(filename):
#    with open(filename, 'w') as f:
#        event = EventImport.get(id)
#        if not event:
#            print 'writing', filename
#            page = page_fetch(link)
#            event_id = handle_page(page)
#            sync_db(id, event_id)
#            f.write(page)

def main():
    for url,user_id,zsite_id in DOUBAN_SITE_LIST:
        danxiangjie = DoubanSite(url,user_id,zsite_id)


if __name__ == '__main__':
    main()
