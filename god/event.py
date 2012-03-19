#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from model.event import Event, event_review_yes, event_review_no, EVENT_STATE_TO_REVIEW, event_new
from model.po import Po
from zkit.page import page_limit_offset
from model.event import Event
from ctrl.zsite.po_event import po_event_edit_get, po_event_edit_post
#from model.sync import mq_sync_po_by_zsite_id

PAGE_LIMIT = 50

@urlmap('/event/review')
class EventReview(Base):
    def get(self):
        qs = Event.where(state=EVENT_STATE_TO_REVIEW).order_by('id')[:1]
        o = None
        if qs:
            o = qs[0]
        self.render(event=o)


@urlmap('/event')
@urlmap('/event-(\d+)')
class EventIndex(Base):
    def get(self, n=1):
        qs = Event.where()
        total = qs.count()
        page, limit, offset = page_limit_offset(
            '/event-%s',
            total,
            n,
            PAGE_LIMIT,
        )
        li = qs.order_by('id desc')[offset: offset + limit]
        Po.mc_bind(li, 'po', 'id')
        self.render(
            'god/event/event_page.htm',
            stat=0,
            li=li,
            page=page,
        )


@urlmap('/event/(\d+)')
@urlmap('/event/(\d+)-(\d+)')
class EventPage(Base):
    def get(self, state, n=1):
        state = int(state)
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
            stat=state,
            li=li,
            page=page,
        )


@urlmap('/event/state/(\d+)/(0|1)')
class EventState(Base):
    def post(self, id, state):
        state = int(state)
        if state:
            event_review_yes(id)
            #e = Event.mc_get(id)
            #mq_sync_po_by_zsite_id(e.zsite_id,id)
        else:
            txt = self.get_argument('txt')
            event_review_no(id, txt)
        self.finish('{}')


@urlmap('/event/edit/(\d+)')
class EventEdit(Base):
    def _event(self, id):
        event = Event.mc_get(id)
        if not event:
            return self.redirect('/')
        return event

    def get(self, id):
        event = self._event(id)
        if event:
            return po_event_edit_get(self, event)

    def post(self, id):
        event = self._event(id)
        if event:
            event = po_event_edit_post(self, id, event, True, event_new)
            if event:
                return self.get(id)

@urlmap('/event/po/edit/(\d+)')
class EventPoEdit(Base):
    def get(self, id):
        event = Event.mc_get(id)
        po = event.po
        self.render(po=po)

    def post(self, id):
        po = Po.mc_get(id)
        name = self.get_argument('name', None)
        txt = self.get_argument('txt', None)
        if name:
            po.name_ = name
            po.save()
        if txt:
            po.txt_set(txt)
        self.redirect('/event')
