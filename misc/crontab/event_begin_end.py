#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from time import time
from zkit.single_process import single_process
from zweb.orm import ormiter
from model.event import Event, event_begin2now, event_end, EVENT_STATE_NOW, EVENT_STATE_BEGIN
from model.kv_misc import kv_int_call, KV_EVENT_STATE


def event_begin(begin, end):
    for i in ormiter(Event, 'state=%s and begin_time>%s' % (EVENT_STATE_BEGIN, begin)):
        event_begin2now(i)

def _event_end(end):
    end = end + 8*60
    for i in ormiter(Event, 'state=%s and end_time<=%s' % (EVENT_STATE_NOW, end)):
        event_end(i)

def event_begin_end(begin):
    end = time()  // 60 + 1
    event_begin(begin, end)
    _event_end(end)
    return end

@single_process
def main():
    kv_int_call(KV_EVENT_STATE, event_begin_end)

if __name__ == '__main__':
    main()

#    end = time()  // 60  + 10*60
#    print end
#    for i in ormiter(Event, 'state=%s ' % (EVENT_STATE_NOW)):
#        print i.end_time , i.id
#
    #e = Event.mc_get(10206300)
    #print e.state
#    from model.po import Po
#    end = (time() - timezone) // 60 + 1
#    
#    for i in ormiter(Event, ' end_time<=%s' % ( end)):
#        po = Po.mc_get(i.id)
#        print po.name, i.end_time
#    print time()/60
