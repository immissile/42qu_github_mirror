#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import JLoginBase, Base
from ctrl._urlmap.j import urlmap
from model.po_recommend import po_recommend_new
from model.po import Po, PO_SHARE_FAV_CID
from yajl import dumps
from model.vote import vote_down_x, vote_down, vote_up_x, vote_up
from model.feed_render import MAXINT, PAGE_LIMIT, render_feed_by_zsite_id, FEED_TUPLE_DEFAULT_LEN, dump_zsite
from model.feed import feed_rm
from model.ico import pic_url_with_default
from model.cid import CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_WORD, CID_EVENT
from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
from itertools import groupby
from operator import itemgetter
from model.career import career_dict
from model.zsite import Zsite
from model.po_video import CID_VIDEO, video_link_autoplay
from model.po_tag import tag_name_id_list_by_po_id
from model.event import Event
from zkit.time_format import friendly_time
from model.fav import fav_new, fav_rm
from cgi import escape
from ctrl.j.po import post_reply
from model.zsite import zsite_name_id_dict
from model.po_event import event_feedback_id_get, po_event_notice_list_by_event_id
from model.po_pos import po_pos_mark
from model.event import EVENT_STATE_END , event_joiner_feedback_normal_count , event_joiner_feedback_good_count
from model.zsite_site import zsite_id_list_by_user_id
from model.site_feed import site_po_iter
from model.career import career_current_str

@urlmap('/j/site/feed/(\d+)')
class SiteFeed(JLoginBase):
    def get(self, id):
        id = int(id)
        if id == 0:
            id = MAXINT
        current_user_id = self.current_user_id
        id_list = zsite_id_list_by_user_id(current_user_id)
        result, last_id = site_po_iter(id_list, PAGE_LIMIT, id)

        if result:
            result.append(last_id)

        self.finish(dumps(result))


@urlmap('/j/feed/fav/(\d+)')
class Fav(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        fav_new(current_user_id, id)
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

        sync = self.get_argument('sync', '')
        txt = self.get_argument('txt', '')

        po = Po.mc_get(id)


        if po and po.cid in PO_SHARE_FAV_CID:
            vote_up(current_user_id, id)
            reply_id = None

            if sync == 'true':
                reply_id = post_reply(self, id)

            rec = po_recommend_new(id, current_user_id, txt, reply_id)

        if not self._finished:
            self.finish('{}')

#mq_sync_recommend_by_zsite_id(current_user_id,rec.id)
#sync_recommend(current_user_id,rec.id)


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

        if result:
            site_id_set = set()
            for zsite_id, item_list in result:
                zsite = Zsite.mc_get(zsite_id)
                t = []
                for i in item_list:
                    id = i[1]
                    cid = i[4]
                    rid = i[5]

                    site_id = i[6]
                    if site_id:
                        site_id_set.add(site_id)

                    if len(i) >= FEED_TUPLE_DEFAULT_LEN:
                        after = i[FEED_TUPLE_DEFAULT_LEN:]
                        i = i[:FEED_TUPLE_DEFAULT_LEN]
                    else:
                        after = None


                    if cid not in (CID_WORD, CID_EVENT):
                        i.extend(zsite_tag_id_tag_name_by_po_id(zsite_id, id))

                    if after:
                        i.extend(after)

                    if cid == CID_NOTE:
                        tag_list =  tag_name_id_list_by_po_id(id)
                        i.append(tag_list)

                    t.append(i[1:])

                unit, title = c_dict[zsite_id]
                if zsite:
                    r.append((
                        zsite.cid,
                        zsite.name,
                        zsite.link,
                        unit,
                        title,
                        pic_url_with_default(zsite_id, '219'),
                        t
                    ))
                else:
                    print 'feed_rm %s zsite_id %s'%(id, zsite_id)
                    feed_rm(id)

            r.append(zsite_name_id_dict(site_id_set))
            r.append(last_id)


        result = dumps(r)

        self.finish(result)

@urlmap('/j/po/json/(\d+)')
class PoJson(Base):
    def get(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        if po.can_view(self.current_user_id):
            tag_list = tag_name_id_list_by_po_id(id)

            result = {
                'txt':po.htm,
                'reply_count':po.reply_count,
                'create_time':po.create_time,
                'tag_list':tag_list,
            }
            user = po.user
            if user:
                result['link'] = user.link
                result['user_name'] = " ".join((
                    user.name,
                    career_current_str(user.id)
                ))
            po_pos_mark(current_user_id, po)
        else:
            result = {}

        self.finish(result)

@urlmap('/j/fdtxt/(\d+)')
class FdTxt(Base):
    def get(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        cid = po.cid
        if po.can_view(current_user_id):
            po_pos_mark(current_user_id, po)
            result = po.htm
            if cid == CID_EVENT:
                result = [result]
                event = Event.mc_get(id)
                if event.phone:
                    result.append('<p>联系电话 : %s</p>'%escape(event.phone))
                if event.transport:
                    result.append(
                        '<p>交通方式 : %s</p>'%escape(event.transport)
                    )

                if event.price:
                    result.append('<p>%s 元 / 人</p>'%event.price)


                notice_list = po_event_notice_list_by_event_id(id)
                for notice in notice_list:
                    result.append('<div class="pb14"><div><b>%s</b></div>%s</div>'%(
                        friendly_time(notice.create_time),
                        notice.name_htm
                    ))

                t = []

                if event.join_count:
                    t.append(
                        '<a href="/%s#join_count" target="_blank"><span class="mr3">%s</span>报名</a>'%(
                            event.id ,
                            event.join_count
                        )
                    )

                if event.state < EVENT_STATE_END:
                    t.append('<a href="/event/join/%s" target="_blank">报名参加</a>'%event.id)
                else:
                    nc = event_joiner_feedback_normal_count(id)
                    gc = event_joiner_feedback_good_count(id)
                    if gc:
                        t.append(
'<a href="/%s#feedback_good" target="_blank"><span class="mr3">%s</span>好评</a>'%(
                        id,
                        gc
)
                        )
                    if nc:
                        t.append(
'<a href="/%s#feedback_normal" target="_blank"><span class="mr3">%s</span>反馈</a>'%(
                        id,
                        nc
)
                        )

                if t:
                    result.append(
                        '<p>%s</p>'%(
                            ' , '.join(t)
                        )
                    )

                #if event.state == EVENT_STATE_END:
                #    result.append("")

                result = ''.join(result)
        else:
            result = ''
        self.finish(result)


