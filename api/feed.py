#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.vote import vote_state
from model.feed_render import render_feed_by_zsite_id, MAXINT, PAGE_LIMIT, FEED_TUPLE_DEFAULT_LEN
from model.feed import feed_rt_id
from model.cid import CID_NOTE ,CID_QUESTION

@urlmap('/user/live')
class UserFeed(_handler.ApiBase):
    def get(self, id=MAXINT):
        user_id = int(self.get_argument('user_id'))
        result = render_feed_by_zsite_id(user_id, PAGE_LIMIT, id)
        data = {}
        for i in result:
            id = i[0]
            i.insert(FEED_TUPLE_DEFAULT_LEN, vote_state(user_id, id))
            i.insert(FEED_TUPLE_DEFAULT_LEN, feed_rt_id(user_id, id))
            weibo = {}
            cid = i[4]
            weibo['id'] = i[0]
            weibo['user_name'] = i[1][0]
            weibo['user_link'] = 'http:%s'%i[1][1]
            if i[2]:
                weibo['rt_list'] = i[2]
            weibo['user_id:'] = i[3]
            weibo['cid:'] = i[4]
            weibo['reply_count'] = i[5]
            weibo['timestamp'] = i[6]
            weibo['name'] = i[7]
            if i[8]:
                weibo['rt_id'] = i[8]
            weibo['vote_state'] = i[9]
            weibo['vote'] = i[10]
            if cid == CID_NOTE:
                weibo['txt'] = i[11]
                data[i[0]] = weibo
            elif cid == CID_QUESTION:
                pass


        self.finish(data)


