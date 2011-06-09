#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _env import PREFIX

from zkit.jsdict import JsDict
import default
import getpass
import socket
import config
def prepare(o):
    o.DEBUG = True

default.load(
    JsDict(vars(config)),
    'dev',
    'host.%s'%socket.gethostname(),
    'host.%s_dev'%socket.gethostname(),
    'user.%s'%getpass.getuser(),
    'user.%s_dev'%getpass.getuser(),
)
