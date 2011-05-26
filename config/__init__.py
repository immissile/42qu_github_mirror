#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from os.path import abspath, dirname, join, normpath
import sys
from os.path import abspath, dirname, join, normpath
from hmako.lookup import TemplateLookup

#初始化python的查找路径
PREFIX = normpath(dirname(dirname(abspath(__file__))))
if PREFIX not in sys.path:
    sys.path = [PREFIX] + sys.path

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

def render(htm, **kwds):
    mytemplate = MAKOLOOKUP.get_template(htm)
    return mytemplate.render(**kwds)

