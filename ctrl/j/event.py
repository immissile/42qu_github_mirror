#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.event import EventUser, event_user_yes, event_user_no, event_user_state
from model.state import STATE_DEL, STATE_APPLY, STATE_SECRET, STATE_ACTIVE


@urlmap('/j/event/check/(\d+)/(0|1)')
class EventCheck(JLoginBase):
    def post(self, id, state):
        current_user_id = self.current_user_id
        state = int(state)
        o = EventUser.mc_get(id)
        if o:
            event = o.event
            if event:
                if event.zsite_id == current_user_id and o.state == STATE_APPLY:
                    if state:
                        event_user_yes(o)
                    else:
                        event_user_no(o)
        self.finish('{}')
