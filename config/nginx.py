#!/usr/bin/env python
#coding:utf-8
from __init__ import PREFIX,join
from mako.template import Template
with open(join(PREFIX,"config/nginx/template.conf")) as template:
    TEMPLATE = Template(template.read())

def render_conf(cls):
    print TEMPLATE.render(this=cls())
    return cls

class ConfBase(object):
    @property
    def pic_host(self):
        return self.config.PIC_URL[7:]

    @property
    def pic_path(self):
        return self.config.FS_PATH

    @property
    def fs_host(self):
        return self.config.FS_URL[7:]

    @property
    def fs_path(self):
        return self.config.FS_PATH

    @property
    def god_port(self):
        print dir(self.config)
        return self.config.GOD_PORT

    @property
    def host(self):
        config = self.config
        host = {
            config.SITE_DOMAIN: [config.PORT,]
        }
        return host

    @property
    def root(self):
        return "/home/%s/zpage/static"%self.__class__.__name__.lower()

def load(setting):
    import __init__
    __import__(setting, globals(), locals(), [], -1)
    reload(__init__)
    return __init__

@render_conf
class Yup(ConfBase):
    config = load("conf_yup")


@render_conf
class Zjd(ConfBase):
    config = load("conf_zjd")

@render_conf
class Zuroc(ConfBase):
    config = load("conf_zuroc")


@render_conf
class Work(ConfBase):
    config = load("conf_work")
    host = {
        "42qu.me" : [
            22000,
            22001
        ],
    }
    root = "/home/work/zpage/web/static"

@render_conf
class WorkDev(ConfBase):
    config = load("host_dev_nuva")
    root = "/home/work/zpage/web/static"

