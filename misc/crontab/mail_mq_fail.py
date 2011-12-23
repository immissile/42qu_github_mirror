#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
import datetime
from model.kv_misc import kv_int_call, KV_EVENT_STATE
from model._db import cursor_by_table
from model.mail import sendmail
import time
<<<<<<< local

mail_addr = 'dev@42qu.com'

=======
>>>>>>> other
def event_begin_end(begin):
    pass
<<<<<<< local

=======
    
>>>>>>> other
def main():
    cursor = cursor_by_table('failed_mq')
<<<<<<< local
    now = datetime.datetime.now().strftime('%Y%m%d')
=======
    now  = datetime.datetime.now().strftime('%Y%m%d')
>>>>>>> other
    cursor.execute('select id,body,exc,func,time from failed_mq where time>%s'%str(int(now)-1))

    out = ''
<<<<<<< local
    for id, body, exc, func, ctime in cursor.fetchall():
        out += '---------Traceback----------\n'
        out += exc
        out += '\n--------function----------\n'
        out += func
        out += '\n-----------time-----------\n'
        out += ctime
        out += '\n******************************\n'

    sendmail(now, out, mail_addr, name=now+'42qu_mq_error')
=======
    for id,body,exc,func,ctime in cursor.fetchall():
        out+='---------Traceback----------\n'
        out+=exc
        out+='\n--------function----------\n'
        out+=func
        out+='\n-----------time-----------\n'
        out+=ctime
        out+='\n******************************\n'
    
    sendmail(now,out,'guohaochuan@gmail.com',name='42qu')
>>>>>>> other

if __name__ == '__main__':
    main()
