#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import datetime
from model.kv_misc import kv_int_call, KV_EVENT_STATE
from model._db import cursor_by_table
from model.mail import sendmail
import time

mail_addr = 'dev@42qu.com'

def event_begin_end(begin):
    pass

def main():
    cursor = cursor_by_table('failed_mq')
    now = datetime.datetime.now().strftime('%Y%m%d')
    cursor.execute('select id,body,exc,func,time from failed_mq where time>%s'%str(int(now)-1))

    out = ''
    for id, body, exc, func, ctime in cursor.fetchall():
        out += '---------Traceback----------\n'
        out += exc
        out += '\n--------function----------\n'
        out += func
        out += '\n-----------time-----------\n'
        out += ctime
        out += '\n******************************\n'

    sendmail(now, out, mail_addr, name=now+'42qu_mq_error')

if __name__ == '__main__':
    main()
