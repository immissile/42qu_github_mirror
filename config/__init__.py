#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from os.path import abspath, dirname, join, normpath
from hmako.lookup import TemplateLookup

from conf import *

GOD_PORT = PORT + 11

SITE_DOMAIN_SUFFIX = '.%s' % SITE_DOMAIN

SITE_URL = 'http://%s' % SITE_DOMAIN


HTM_PATH = join(dirname(dirname(abspath(__file__))), 'htm')

MAKOLOOKUP = TemplateLookup(
    directories=HTM_PATH,
    module_directory='/tmp/%s'%HTM_PATH.strip('/').replace('/', '.'),
    disable_unicode=True,
    encoding_errors='ignore',
    default_filters=['str', 'h'],
    filesystem_checks=DEBUG,
    input_encoding='utf-8',
    output_encoding=''
)

SENDER_NAME = SITE_DOMAIN

def render(htm, **kwds):
    mytemplate = MAKOLOOKUP.get_template(htm)
    return mytemplate.render(**kwds)


DB_HOST_MAIN = '%s:%s:%s:%s:%s' % (MYSQL_HOST, MYSQL_PORT, MYSQL_MAIN, MYSQL_USER, MYSQL_PASSWD)

DB_CONFIG = {
    'main': {
        'master': DB_HOST_MAIN,
        'tables': (
            '*'
        )
    }
}
