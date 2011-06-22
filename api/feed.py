#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.vote import vote_state
from model.feed_render import render_feed_by_zsite_id, MAXINT, PAGE_LIMIT, FEED_TUPLE_DEFAULT_LEN
from model.feed import feed_rt_id
from model.cid import CID_NOTE ,CID_QUESTION
from yajl import dumps

@urlmap('/user/live')
class UserFeed(_handler.ApiBase):
    def get(self, id=MAXINT):
        user_id = int(self.get_argument('user_id'))
        result = render_feed_by_zsite_id(user_id, PAGE_LIMIT, id)
        data = []
        for i in result:
            id = i[0]
            cid = i[4]
            weibo = {}


            rt_id = feed_rt_id(user_id, id)
            if rt_id:
                weibo['rt_id'] = rt_id
            weibo['vote_state'] = vote_state(user_id, id)


            weibo['id'] = i[0]
            weibo['user_name'] = i[1][0]
            weibo['user_link'] = 'http:%s'%i[1][1]
            if i[2]:
                weibo['rt_list'] = i[2]

            weibo['user_id'] = i[3]
            weibo['cid'] = i[4]
            weibo['reply_count'] = i[5]
            weibo['timestamp'] = i[6]
            weibo['name'] = i[7]
            weibo['vote'] = i[8]

            if cid == CID_NOTE:
                weibo['txt'] = i[9]
            elif cid == CID_QUESTION:
                pass


            data.append(weibo)
        
        self.finish({
            "item":data
        })


