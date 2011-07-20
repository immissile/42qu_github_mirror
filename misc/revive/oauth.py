#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from qu.myconf.config import DB_HOST_ONLINE
from zpage.config import DB_CONFIG
import subprocess
import time
from getpass import getpass

OLD_DB_NAME = DB_HOST_ONLINE.split(':')[2]

host, port, name, user, password = DB_CONFIG['main'].get('master').split(':')
user = 'root'
password = getpass()
SQL = 'mysql -h%s -P%s -u%s -p%s' % (host, port, user, password)

with open('data.sql', 'w') as f:
    for table in (
        'oauth_token',
        'oauth_token_buzz',
        'oauth_token_douban',
        'oauth_token_qq',
        'oauth_token_sina',
        'oauth_token_sohu',
        'oauth_token_twitter',
        'oauth_token_www163',
    ):
        sql = '''
truncate {new}.{table};
insert into {new}.{table} select * from {old}.{table};
'''.format(new=name, old=OLD_DB_NANE, table=table)
        f.write(sql)

subprocess.Popen('%s < data.sql' % SQL, shell=True)
time.sleep(2)
