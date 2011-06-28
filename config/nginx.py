#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _env import PREFIX, join
from mako.template import Template
import default
import socket
from zkit.jsdict import JsDict
import glob
from os import makedirs
from os.path import exists, dirname

CONFIG_DIR = join(PREFIX, 'config/nginx')

with open(join(dirname(CONFIG_DIR), 'template/nginx.conf')) as template:
    TEMPLATE = Template(template.read())

def render_conf(name, base_path, o, port_list=[], zsite_port_list=[]):
    fs_path = base_path+'/static'
    if not port_list:
        port_list = [o.PORT]
    if not zsite_port_list:
        zsite_port_list = [o.ZSITE_PORT]
    txt = TEMPLATE.render(
        this=o,
        port_list=port_list,
        zsite_port_list=zsite_port_list,
        fs_path=fs_path,
        base_path=base_path
    )
    path = join(
            PREFIX, 'config/nginx/%s'%name
        )
    dirpath = dirname(path)
    if not exists(dirpath):
        makedirs(dirpath)

    with open(path, 'w') as w:
        w.write(txt)

def render(name, host, user, port_list=None):
    o = default.load(
        JsDict(), 'host.%s'%host, 'user.%s'%user
    )
    print o.SITE_DOMAIN
    render_conf(
        name,
        '/home/%s/zpage'%user,
        o
    )


def render_machine(host, name_list):
    name_list = name_list.strip().split()
    for name in name_list:
        config_name = '%s/%s.conf'%(host, name)
        render(config_name, host, name)

render_machine('krios', """
zuroc
zjd
yup
zwtaoo
silegon
work
""")

render_machine('nuva', """
work
""")

#    render_conf(1)
#@render_conf
#class Work(ConfBase):
#    config_file = "conf_work"
#    host = {
#        "42qu.me" : [
#            22000,
#            22001
#        ],
#    }
#    fs_path = "/home/work/zpage/web/static"
#
#@render_conf
#class WorkDev(ConfBase):
#    config_file = "host_dev_nuva"
#    fs_path = "/home/work/zpage/web/static"
#
