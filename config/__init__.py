#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 初始化python的查找路径
import _env
import default
import getpass
import socket
from zkit.jsdict import JsDict

default.load(
    JsDict(locals()),
    'host.%s' % socket.gethostname(),
    'user.%s' % getpass.getuser(),
)
