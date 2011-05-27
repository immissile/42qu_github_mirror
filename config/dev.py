#!/usr/bin/env python
# -*- coding: utf-8 -*-

from init_env import PREFIX

from zkit.jsdict import JsDict
import default
import getpass
import socket

default.load(
    JsDict(locals()),
    "dev",
    "host.%s"%socket.gethostname(),
    "host.%s_dev"%socket.gethostname(),
    "user.%s"%getpass.getuser(),
    "user.%s_dev"%getpass.getuser(),
)
