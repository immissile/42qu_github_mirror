#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import JLoginBase, Base
from ctrl._urlmap.j import urlmap
from model.vote import vote_state
from model.po import Po, PO_SHARE_FAV_CID
from yajl import dumps
from model.vote import vote_down_x, vote_down, vote_up_x, vote_up
from model.feed_render import MAXINT, PAGE_LIMIT, render_feed_by_zsite_id, FEED_TUPLE_DEFAULT_LEN, dump_zsite
from model.feed import feed_rt, feed_rt_rm, feed_rt_id
from model.ico import pic_url_with_default
from model.cid import CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_WORD, CID_EVENT
from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
from itertools import groupby
from operator import itemgetter
from model.career import career_dict
from model.zsite import Zsite
from model.po_video import CID_VIDEO, video_htm_autoplay
from model.event import Event
from model.fav import fav_add, fav_rm
from cgi import escape
from ctrl.j.po import post_reply

@urlmap('/j/feed/fav/(\d+)')
class Fav(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        fav_add(current_user_id, id)
        self.finish('{}')


@urlmap('/j/feed/unfav/(\d+)')
class UnFav(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        fav_rm(current_user_id, id)
        self.finish('{}')

@urlmap('/j/feed/up/(\d+)')
class FeedUp(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id

        po = Po.mc_get(id)
        if po and po.cid in PO_SHARE_FAV_CID:
            vote_up(current_user_id, id)
            feed_rt(current_user_id, id)

        post_reply(self, id)


@urlmap('/j/feed/(\d+)')
class Feed(JLoginBase):
    def get(self, id):
        id = int(id)
        if id == 0:
            id = MAXINT
        current_user_id = self.current_user_id

        result, last_id = render_feed_by_zsite_id(current_user_id, PAGE_LIMIT, id)
        result = tuple(
            (i, tuple(g)) for i, g in groupby(result, itemgetter(0))
        )
        zsite_id_set = set(
            i[0] for i in result
        )
        c_dict = career_dict(zsite_id_set)

        r = []
        for zsite_id, item_list in result:
            zsite = Zsite.mc_get(zsite_id)
            t = []
            for i in item_list:
                id = i[1]
                cid = i[4]
                rid = i[5]

                if len(i) >= FEED_TUPLE_DEFAULT_LEN:
                    after = i[FEED_TUPLE_DEFAULT_LEN:]
                    i = i[:FEED_TUPLE_DEFAULT_LEN]
                else:
                    after = None

                #        i.extend([
                #            vote_state(current_user_id, id),
                #        ])

                if cid not in (CID_WORD, CID_EVENT):
                    i.extend(zsite_tag_id_tag_name_by_po_id(zsite_id, id))

                if after:
                    i.extend(after)
                t.append(i[1:])

            unit, title = c_dict[zsite_id]
            r.append((
                zsite.name,
                zsite.link,
                unit,
                title,
                pic_url_with_default(zsite_id, '219'),
                t
            ))
        r.append(last_id)
        result = dumps(r)
        self.finish(result)


@urlmap('/j/fdtxt/(\d+)')
class FdTxt(Base):
    def get(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        cid = po.cid
        if po.can_view(current_user_id):
            result = po.htm
            if cid == CID_EVENT:
                result = [result]
                event = Event.mc_get(id)
                result.append('<p>联系电话 : %s</p>'%escape(event.phone))
                result.append(
                    '<p>交通方式 : %s</p>'%escape(event.transport)
                )
                if event.price:
                    result.append('<p>%s 元 / 人</p>'%event.price)
                result = ''.join(result)
        else:
            result = ''
        self.finish(result)

@urlmap('/j/fdvideo/(\d+)')
class FdVideo(Base):
    def get(self, id):
        po = Po.mc_get(id)
        if po and po.cid == CID_VIDEO:
            self.finish(video_htm_autoplay(po.rid, id))

