#!/usr/bin/env python
#coding:utf-8
from mako.lookup import TemplateLookup
from os.path import abspath, dirname, join, normpath
from zpage_ctrl import DEBUG

HTM_PATH = join(dirname(dirname(abspath(__file__))),"htm")


MAKOLOOKUP = TemplateLookup(
    directories=HTM_PATH,
    module_directory='/tmp/%s'%HTM_PATH.strip("/").replace("/","."),
    disable_unicode=True,
    encoding_errors="ignore",
    default_filters=['str', 'h'],
    filesystem_checks=DEBUG,
    input_encoding='utf-8',
    output_encoding=''
)


def render(htm, **kwds):
    mytemplate = MAKOLOOKUP.get_template(htm)
    return mytemplate.render(**kwds)
