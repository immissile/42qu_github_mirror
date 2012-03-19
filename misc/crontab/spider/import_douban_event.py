#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.spider import Rolling, NoCacheFetch, GSpider
from model._db import Model, McModel, McNum
from model.po import po_new
from datetime import datetime
from model.po_event import po_event_pic_new , EVENT_CID, po_event_feedback_new
from model.event import Event, event_init2to_review
from model.state import STATE_SECRET
from model.cid import CID_EVENT, CID_NOTICE_EVENT_JOINER_FEEDBACK
from model.event import Event, EVENT_JOIN_STATE_YES, EVENT_JOIN_STATE_FEEDBACK_GOOD, EVENT_JOIN_STATE_FEEDBACK_NORMAL, event_new_if_can_change, EventJoiner, event_joiner_user_id_list, event_joiner_get, event_joiner_state, last_event_by_zsite_id, event_new
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
from zkit.earth import PID2NAME, PLACE_L1L2
import re
from model.days import time_by_string, datetime_to_minutes
from model.event import EVENT_CID_CN
from zkit.location_douban import DOUBAN2ID

EVENT_DICT = dict([(unicode(v), k) for k, v in EVENT_CID_CN])

PLACE_DICT = dict([(unicode(v), k) for k, v in PID2NAME.items()])


class ImportDoubanEvent(Model):
    pass


DOUBAN_SITE_LIST = (
        # url , user_id , zsite_id
        (117123  , 10074584, 10199666), #单向街      
        (1409398 , 10000065, 10091192), #Python     
        (326387  , 10018609, 10133826), #真人图书馆  
        (1226483 , 10010448, 10126347), #科学松鼠会 
        (4134513 , 10018576, 10200247), #豆瓣公开课 
        (3954604 , 10019039, 10200245), #草地音乐 
        (1890616 , 10026843, 10203860), #果壳网
        (1467576 , 10209245, 10209311), #上海朋歌
        (1332535 , 10209208, 10209312), #上海幽默双关语
        (1293724 , 10209356, 10211628), #广州漂流木塔羅占星工坊
        (1224229 , 10211943, 10212100), #广州我们的图书馆
)

def location_finder(name):
    if name in DOUBAN2ID:
        return DOUBAN2ID[name]
    else:
        if name in PLACE_DICT:
            return PLACE_DICT[name]
    return 1

def save_event(self, phone, address, begin_time, end_time, title, intro, douban_event_id , typ):

    begin_time = time_by_string(begin_time)
    end_time = time_by_string(end_time)

    if begin_time < datetime.now():
        return None

    if typ in EVENT_DICT:
        event_cid = EVENT_DICT[typ]
    else:
        event_cid = EVENT_DICT[u'其他']

    city = address[0]
    place = address[1]
    if len(address) == 2:
        address = address[1]
    else:
        address = address[2]


    city_pid = location_finder(city)
    pid = location_finder(place)

    if pid not in PLACE_L1L2[city_pid]:
        pid = city_pid

    begin = datetime_to_minutes(begin_time)
    end = datetime_to_minutes(end_time)

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
        0,
        limit_up,
        limit_down,
        phone,
        0,
        id
    )

    id = event.id


    po = po_new(CID_EVENT, self.user_id, '', STATE_SECRET , id=id, zsite_id=self.zsite_id)
    if po:
        po.name_ = title
        po.txt_set(htm2txt(intro)[0])
        po.save()

        event_init2to_review(id)
        import_douban_event = ImportDoubanEvent.get_or_create(id=int(douban_event_id))
        import_douban_event.event_id = id
        import_douban_event.save()

        return event

def save_pic(pic, pic_url, event):
    pic = picopen(pic)
    if not pic:
        return
    else:
        pic_id = po_event_pic_new(event.zsite_id, pic)
        event.pic_id = pic_id
        event.save()

class ParseEventIndex(object):
    def __init__(self, user_id , zsite_id):
        self.zsite_id = zsite_id
        self.user_id = user_id

    def __call__(self, html, url):
        html = txt_wrap_by('<ul class="list-m">', '</ul>', html)
        items = txt_wrap_by_all('<li class="item">', '</div>', html)
        if not items:
            items = txt_wrap_by_all('<h3><a', '</h3', html)

        links = []
        for item in items:
            link = txt_wrap_by('href="', '"', item)

            id = txt_wrap_by('http://www.douban.com/event/', '/', link)
            id = int(id)
            event = ImportDoubanEvent.get(id)
            if not event:
                yield self.parse_event_page, link , id
                ImportDoubanEvent(id=id,event_id=0).save()
 
    def parse_event_page(self, page, url, douban_event_id):
        title = txt_wrap_by('h1>', '</h1>', page)
        pic_url = txt_wrap_by('href="', '"', txt_wrap_by('class="album_photo"', '>', page))
        begin_time = txt_wrap_by('ail">', '<', txt_wrap_by('开始时间', '/div', page))
        end_time = txt_wrap_by('ail">', '<', txt_wrap_by('结束时间', '/div', page))
        address = unicode(txt_wrap_by('span>', '<', txt_wrap_by('地点', 'br/>', txt_wrap_by('class="obmo">', '</div', page)))).split(' ')
        typ = txt_wrap_by('类型: </span>', '<br/', page)
        typ = txt_wrap_by('">', '/', typ)
        intro = txt_wrap_by('play:none">', '<a href="javasc', page)
        phone = txt_wrap_by('电话', '<br/', intro)
        if not intro:
            intro = txt_wrap_by('<div class="wr">', '</div>', page)
        if phone:
            phone = phone.replace('：', '').replace(':', '')

        event = save_event(self, phone, address, begin_time, end_time, title, intro, douban_event_id, typ)

        if event:
            yield save_pic, pic_url, event


def main():
    url_list = []
    for url, user_id, zsite_id in DOUBAN_SITE_LIST:
        url_list.append((ParseEventIndex(user_id, zsite_id), 'http://site.douban.com/widget/events/%s/'%url))

    #self.url, self.user_id, self.zsite_id = url, user_id, zsite_id
    headers = {
        'Cookie':'bid=i9gsK/lU40A',
    }
    fetcher = NoCacheFetch(10, headers=headers)
    spider = Rolling( fetcher, url_list )
    spider_runner = GSpider(spider, workers_count=1)
    spider_runner.start()

if __name__ == '__main__':
    main()
