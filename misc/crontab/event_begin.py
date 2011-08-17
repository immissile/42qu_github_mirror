#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from time import time
from zkit.single_process import single_process
from zweb.orm import ormiter
from model.event import Event, event_begin2now


@single_process
def event_begin():
    begin_time = time() // 60 + 1
    for i in ormiter(Event, 'state=%s and begin_time<%s' % (EVENT_STATE_BEGIN, begin_time)):
        event_begin2now(i)

if __name__ == '__main__':
    event_begin()
