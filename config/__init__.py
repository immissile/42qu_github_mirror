#!/usr/bin/env python
# -*- coding: utf-8 -*-

#初始化python的查找路径
#coding:utf-8
from init_env import PREFIX

from zkit.jsdict import JsDict
import default
import getpass
import socket

default.load(
    JsDict(locals()),
    "host.%s"%socket.gethostname(),
    "user.%s"%getpass.getuser(),
)

