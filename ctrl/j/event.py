#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.event import EventJoiner, event_joiner_yes, event_joiner_no, event_joiner_state
from model.state import STATE_DEL, STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from model.buzz import mq_buzz_event_join_new


@urlmap('/j/event/check/(\d+)/(0|1)')
class EventCheck(JLoginBase):
    def post(self, id, state):
        current_user_id = self.current_user_id
        state = int(state)
        o = EventJoiner.mc_get(id)
        if o:
            event = o.event
            if event:
                if event.zsite_id == current_user_id and o.state == STATE_APPLY:
                    if state:
                        event_joiner_yes(o)
                        mq_buzz_event_join_new(o.user_id, o.event_id)
                    else:
                        event_joiner_no(o)
        self.finish('{}')
