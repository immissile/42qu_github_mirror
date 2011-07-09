#!/usr/bin/env python
# -*- coding: utf-8 -*-
import init_env
from zpage.config import DB_CONFIG
import subprocess
import time

host, port, name, user, password = DB_CONFIG['main'].get('master').split(':')
print host, port, name, user, password
SQL = 'mysql -h%s -P%s -u%s -p%s' % (host, port, user, password)

subprocess.Popen('%s < data_migration.sql' % SQL, shell=True)
time.sleep(2)

from qu.mysite.model.const import man
from qu.mysite.model.const.man import CID_MAN, STATE_APPLY, STATE_APPLYED, STATE_BAN, STATE_ACTIVE, A_STATE, STATE_DEL, STATE_VERIFY, STATE_RECALLED


from qu.mysite.model.const.man import STATE_BAN, STATE_DEL, STATE_TO_VERIFY, STATE_APPLY, STATE_APPLYED, STATE_ACTIVE, STATE_VERIFY, STATE_TODO, STATE_REAL

from zpage.model.zsite import Zsite, ZSITE_STATE_BAN, ZSITE_STATE_NO_MAIL, ZSITE_STATE_NO_PASSWORD, ZSITE_STATE_APPLY, ZSITE_STATE_ACTIVE, ZSITE_STATE_FAILED_VERIFY, ZSITE_STATE_WAIT_VERIFY, ZSITE_STATE_VERIFY_CANNOT_REPLY, ZSITE_STATE_CAN_REPLY, ZSITE_STATE_VERIFY

ZSITE_STATE_TUPLE = (
    (STATE_REAL, ZSITE_STATE_VERIFY),
    (STATE_ACTIVE, ZSITE_STATE_ACTIVE),
    (STATE_APPLY, ZSITE_STATE_APPLY),
    (STATE_TO_VERIFY, ZSITE_STATE_APPLY),
)

for old, new in ZSITE_STATE_TUPLE:
    sql = 'update zpage.zsite set state=%s where state=%s;' % (new, old)
    sql = '%s -e "%s"' % (SQL, sql)
    print sql
    subprocess.Popen(sql, shell=True)
    time.sleep(2)
