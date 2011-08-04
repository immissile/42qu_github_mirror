#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from model.event import Event
from model.money import trade_event_new


class EventBase(LoginBase):
    template = None

    def event(self, id):
        o = Event.mc_get(id)
        if o:
            if o.zsite_id == self.zsite_id:
                return o
            return self.redirect(o.link)
        return self.redirect('/')

    def get(self, id):
        event = self.event(id)
        if event is None:
            return

        return self.render(
            self.template,
            event=event,
        )


@urlmap('/event/in/(\d+)')
class EventIn(EventBase):
    def post(self, id):
        event = self.event(id)
        if event is None:
            return

        if event.price:
            return self.redirect('/event/pay/%s' % id)


@urlmap('/event/pay/(\d+)')
class EventPay(EventBase):
    def event(self, id):
        event = super(EventPay, self).event(id)
        if event.price:
            return event
        return self.redirect(event.link)

    def post(self, id):
        event = self.event(id)
        if event is None:
            return
