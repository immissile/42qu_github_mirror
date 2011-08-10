#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.event import Event, event_review_yes, event_review_no, EVENT_STATE_TO_REVIEW
from model.po import Po
from zkit.page import page_limit_offset


PAGE_LIMIT = 50

@urlmap('/event/review')
class EventReview(Base):
    def get(self):
        qs = Event.where(state=EVENT_STATE_TO_REVIEW).order_by('id')[:1]
        o = None
        if qs:
            o = qs[0]
        self.render(event=o)


@urlmap('/event/(\d+)')
@urlmap('/event/(\d+)-(\d+)')
class EventPage(Base):
    def get(self, state, n=1):
        qs = Event.where(state=state)
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/event/%s-%%s' % state,
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        Po.mc_bind(li, 'po', 'id')
        self.render(
            li=li,
            page=page,
        )


@urlmap('/event/state/(\d+)/(0|1)')
class EventState(Base):
    def post(self, id, state):
        state = int(state)
        if state:
            event_review_yes(id)
        else:
            txt = self.get_argument('txt')
            event_review_no(id, txt)
        self.finish('{}')
