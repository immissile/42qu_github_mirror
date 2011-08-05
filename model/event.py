#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel, McCache, McCacheA, McLimitA, McNum
from state import STATE_DEL, STATE_APPLY, STATE_SECRET, STATE_ACTIVE
from time import time
from zkit.attrcache import attrcache


class Event(McModel):

    @attrcache
    def zsite(self):
        return Zsite.mc_get(self.zsite_id)

    @attrcache
    def link(self):
        o = self.zsite
        return '%s/%s' % (o.link, self.id)


STATE_NO = STATE_DEL
STATE_NEW = STATE_APPLY
STATE_YES = STATE_ACTIVE


class EventUser(McModel):
    pass


mc_event_user_get = McCache('EventUserGet.%s')

@mc_event_user_get('{event_id}_{user_id}')
def event_user_get(event_id, user_id):
    o = EventUser.get(event_id=event_id, user_id=user_id)
    if o:
        return o.id
    return 0

def event_user_state(event_id, user_id):
    id = event_user_get(event_id, user_id)
    o = EventUser.mc_get(id)
    if o:
        return o.state
    return 0

def event_user_new(event_id, user_id):
    id = event_user_get(event_id, user_id)
    o = EventUser.mc_get(id)
    if o and o.state >= STATE_APPLY:
        return
    now = int(time())
    if not o:
        o = EventUser.get_or_create(event_id=event_id, user_id=user_id)
    o.state = STATE_APPLY
    o.create_time = now
    o.save()
    if not o:
        mc_event_user_get.set('%s_%s' % (event_id, user_id), o.id)
    return o

def event_user_no(event_id, user_id):
    id = event_user_get(event_id, user_id)
    o = EventUser.mc_get(id)
    if o:
        o.state = STATE_DEL
        o.save()

def event_user_yes(event_id, user_id):
    id = event_user_get(event_id, user_id)
    o = EventUser.mc_get(id)
    if o:
        o.state = STATE_ACTIVE
        o.save()

if __name__ == '__main__':
    pass
