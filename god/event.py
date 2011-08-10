#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.user_mail import mail_by_user_id
from model.mail import sendmail
from model.event import Event, EVENT_STATE_TO_REVIEW
from model.po import Po
from zkit.page import page_limit_offset


PAGE_LIMIT = 50

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
        event = Event.mc_get(id)
        state = int(state)
        if event:
            if state:
                pass
            else:
                pass
        self.finish('{}')
