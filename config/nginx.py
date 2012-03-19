#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _env import PREFIX
from mako.template import Template
import default
import socket
from zkit.jsdict import JsDict
from os import makedirs
from os.path import exists, dirname, join

CONFIG_DIR = join(PREFIX, 'config/nginx')

with open(join(dirname(CONFIG_DIR), 'template/nginx.conf')) as template:
    TEMPLATE = Template(template.read())

def render_conf(name, base_path, o):
    fs_path = base_path+'/static'

    port_list = o.PORT
    if type(port_list) not in (list, tuple):
        port_list = [port_list]

    god_port_list = o.GOD_PORT
    if type(god_port_list) not in (list, tuple):
        god_port_list = [god_port_list]

    api_port_list = o.API_PORT
    if type(api_port_list) not in (list, tuple):
        api_port_list = [api_port_list]

    rpc_port_list = o.RPC_PORT
    if type(rpc_port_list) not in (list, tuple):
        rpc_port_list = [rpc_port_list]


    txt = TEMPLATE.render(
        this=o,
        fs_path=fs_path,
        project_name=o.MYSQL_MAIN,
        base_path=base_path,
        port_list=port_list,
        god_port_list=god_port_list,
        rpc_port_list=rpc_port_list,
        api_port_list=api_port_list,
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
    if type(name_list) is str:
        name_list = name_list.strip().split()

    for name in name_list:
        config_name = '%s/%s.conf'%(host, name)
        render(config_name, host, name)


import socket
hostname = socket.gethostname()

render_machine(hostname, __import__('host_user.%s'%hostname, fromlist=['host_user']).USER)


#render_machine('krios', """
#huhuchen
#zuroc
#wooparadog
#work
#realfex
#""")
#
#render_machine('nuva', """
#work
#""")
#
#render_machine('potato', """
#work
#istarsea
#""")
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
