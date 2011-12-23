#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import datetime
from model.kv_misc import kv_int_call, KV_EVENT_STATE
from model._db import cursor_by_table
from model.mail import sendmail
import time
from config import MQ_FAIL_MAIL_ADDR



def main():
    cursor = cursor_by_table('failed_mq')
    now = datetime.datetime.now().strftime('%Y%m%d')
    cursor.execute('select id,body,exc,func,time from failed_mq where time>%s'%str(int(now)-1))

    out = []
    for id, body, exc, func, ctime in cursor.fetchall():
        out.append('---------Traceback----------\n')
        out.append(exc)
        out.append('\n--------function----------\n')
        out.append(func)
        out.append('\n-----------time-----------\n')
        out.append(ctime)
        out.append('\n******************************\n')
    sendmail(now,''.join(out), MQ_FAIL_MAIL_ADDR, name='failed_mq')

if __name__ == '__main__':
    main()
