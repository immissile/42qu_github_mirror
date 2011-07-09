#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.myconf.config import DB_HOST_ONLINE
from zpage.config import DB_CONFIG
import subprocess
import time

from qu.mysite.model.const.man import STATE_BAN, STATE_DEL, STATE_TO_VERIFY, STATE_APPLY, STATE_APPLYED, STATE_ACTIVE, STATE_VERIFY, STATE_TODO, STATE_REAL

from zpage.model.zsite import Zsite, ZSITE_STATE_BAN, ZSITE_STATE_NO_MAIL, ZSITE_STATE_NO_PASSWORD, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE, ZSITE_STATE_FAILED_VERIFY, ZSITE_STATE_WAIT_VERIFY, ZSITE_STATE_VERIFY_CANNOT_REPLY, ZSITE_STATE_CAN_REPLY, ZSITE_STATE_VERIFY

ZSITE_STATE_TUPLE = (
    (STATE_REAL, ZSITE_STATE_VERIFY),
    (STATE_ACTIVE, ZSITE_STATE_ACTIVE),
    (STATE_APPLY, ZSITE_STATE_APPLY),
    (STATE_TO_VERIFY, ZSITE_STATE_APPLY),
)

oldname = DB_HOST_ONLINE.split(':')[2]

host, port, name, user, password = DB_CONFIG['main'].get('master').split(':')
print host, port, name, user, password
SQL = 'mysql -h%s -P%s -u%s -p%s' % (host, port, user, password)

with open('data.sql', 'w') as f:
    with open('data_migration.sql') as f2:
        s = f2.read()
        f.write(s.replace('qu', oldname))
        for old, new in ZSITE_STATE_TUPLE:
            sql = 'update zpage.zsite set state=%s where state=%s;' % (new, old)
            f.write(sql)

subprocess.Popen('%s < data.sql' % SQL, shell=True)
time.sleep(2)
#
#
#for old, new in ZSITE_STATE_TUPLE:
#    sql = 'update zpage.zsite set state=%s where state=%s;' % (new, old)
#    sql = '%s -e "%s"' % (SQL, sql)
#    print sql
#    subprocess.Popen(sql, shell=True)
#    time.sleep(2)
