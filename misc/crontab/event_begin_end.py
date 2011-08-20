#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from time import time
from zkit.single_process import single_process
from zweb.orm import ormiter
from model.event import Event, event_begin2now, event_end, EVENT_STATE_NOW, EVENT_STATE_BEGIN
from model.kv_misc import kv_int_call, KV_EVENT_STATE


def event_begin(begin, end):
    for i in ormiter(Event, 'state=%s and begin_time>%s and begin_time<=%s' % (EVENT_STATE_BEGIN, begin, end)):
        event_begin2now(i)

def _event_end(begin, end):
    for i in ormiter(Event, 'state=%s and end_time>%s and end_time<=%s' % (EVENT_STATE_NOW, begin, end)):
        event_end(i)

def event_begin_end(begin):
    end = time() // 60 + 1
    event_begin(begin, end)
    _event_end(begin, end)
    return end

@single_process
def main():
    kv_int_call(KV_EVENT_STATE, event_begin_end)

if __name__ == '__main__':
    main()
