#!/usr/bin/env python
#coding:utf-8
from init_env import PREFIX, join
from mako.template import Template
import default
import socket
from zkit.jsdict import JsDict
import glob

CONFIG_DIR = join(PREFIX, "config/nginx/")

with open(CONFIG_DIR+"template.conf") as template:
    TEMPLATE = Template(template.read())

def render_conf(name, fs_path, o, port_list=None):
    if not port_list:
        port_list = [o.PORT]
    txt = TEMPLATE.render(
        this=o,
        port_list=port_list,
        fs_path=fs_path
    )
    with open(join(
            PREFIX, "config/nginx/%s"%name
        ), "w") as w:
        w.write(txt)

def render(name, host, user, port_list=None):
    o = default.load(
        JsDict(), "host.%s"%host, "user.%s"%user
    )
    render_conf(
        name,
        "/home/%s/zpage/static"%name,
        o
    )

def render_machine(host, name_list):
    name_list = name_list.strip().split()
    with open(CONFIG_DIR+"%s.conf"%host, "w") as config:
        for name in name_list:
            config_name = "%s_%s.conf"%(host, name)
            render(config_name, host, name)
            config.write("include %s;\n"%config_name)

render_machine("krios", """
zuroc
zjd
yup
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
