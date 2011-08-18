#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from time import time
from zkit.single_process import single_process
from zweb.orm import ormiter
from model.event import Event, event_begin2now, event_end_mail, EVENT_STATE_END, EVENT_STATE_BEGIN


@single_process
def event_begin():
    begin_time = time() // 60 + 1
    for i in ormiter(Event, 'state=%s and begin_time<%s' % (EVENT_STATE_BEGIN, begin_time)):
        event_begin2now(i)

@single_process
def event_end():
    end_time = time() // 60 + 1
    for i in ormiter(Event, 'state=%s and end_time>%s' % (EVENT_STATE_END, end_time)):
        event_end_mail(i)
    

if __name__ == '__main__':
    event_begin()
    event_end()
