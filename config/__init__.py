#!/usr/bin/env python
# -*- coding: utf-8 -*-

#初始化python的查找路径
#coding:utf-8
from init_env import PREFIX
import default
from zkit.jsdict import JsDict

self = JsDict(locals())
for _ in (
    default.prepare,
    default.finish,
):
    _(self)

del _
del self
del default
del JsDict
