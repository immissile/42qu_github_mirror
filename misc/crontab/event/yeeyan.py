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
import os.path as path
from xml.sax.saxutils import unescape
from zkit.htm2txt import htm2txt
from zkit.spider import Rolling, Fetch, NoCacheFetch, GCrawler
from time import sleep
from os.path import exists
import os.path
from zkit.earth import PID2NAME
import re
from yajl import dumps
from hashlib import md5
from model.days import time_by_string, datetime_to_minutes
import threading

FILE_LOCK = threading.RLock()
CURRNET_PATH = path.dirname(path.abspath(__file__))
writer = open('yeeyan.data','w')

def name_builder(url):
    return os.path.join(CURRNET_PATH,"yeeyan", md5(url).hexdigest())

def parse_page(page, url):
    title = txt_wrap_by('<title>译言网 | ', '</ti', page)
    tags_wrapper = txt_wrap_by('class="tags bdr">', '</div', page)
    tags = txt_wrap_by_all('>', '</a', tags_wrapper)
    author = txt_wrap_by('<h2 id="user_info"', '</a', page)
    rating = txt_wrap_by('已有<span class="number">', '</span', page)
    reply_wrapper_list = txt_wrap_by_all('class="comment_content">', '</ul', page)
    reply_list = []
    for reply_wrapper in reply_wrapper_list:
        reply_list.append(txt_wrap_by('<p>', '</p', reply_wrapper))

    out = dumps([url, title, tags, author, rating , reply_list])
    with FILE_LOCK:
        f.write(out+"\n")

def parse_index(page, url):
    link_wrapper_list = txt_wrap_by_all('<h5 clas', '</h5', page)
    link_list = []
    for link_wrapper in link_wrapper_list:
        url = txt_wrap_by('href="', '"', link_wrapper)
        if not exists(name_builder(url)):
            yield parse_page, url

def yeeyan_url_builder():
    for page in xrange(1, 5001):
        yield parse_index, 'http://article.yeeyan.org/list_a?page=%s'%str(page)

def main():
    headers = {
        'Cookie':'bid=i9gsK/lU40A',
    }

    fetcher = NoCacheFetch(0, headers=headers)
    spider = Rolling( fetcher, yeeyan_url_builder() )
    spider_runner = GCrawler(spider, workers_count=100)
    spider_runner.start()

if __name__ == '__main__':
    main()
