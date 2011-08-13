#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.event import EventJoiner, event_joiner_yes, event_joiner_no, event_joiner_state
from model.event import EVENT_JOIN_STATE_NO, EVENT_JOIN_STATE_NEW, EVENT_JOIN_STATE_YES, EVENT_JOIN_STATE_END, EVENT_JOIN_STATE_REVIEW


@urlmap('/j/event/check/(\d+)/(0|1)')
class EventCheck(JLoginBase):
    def post(self, id, state):
        current_user_id = self.current_user_id
        state = int(state)
        o = EventJoiner.mc_get(id)
        if o:
            event = o.event
            o_state = o.state
            if event:
                if event.can_admin(current_user_id):
                    if state:
                        if o_state == EVENT_JOIN_STATE_NEW:
                            event_joiner_yes(o)
                    else:
                        if o_state in (EVENT_JOIN_STATE_NEW, EVENT_JOIN_STATE_YES):
                            txt = self.get_argument('txt', '')
                            if txt:
                                event_joiner_no(o, txt)
        self.finish('{}')
