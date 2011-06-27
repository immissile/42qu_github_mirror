#!/usr/bin/env python
# -*- coding: utf-8 -*-

from _db import Model, McModel, McCache, McLimitM, McNum
from gid import gid

class BuzzSys(McModel):
    pass

def buzz_sys_new(htm):
    id = gid()
    bs = BuzzSys(id=id, htm=htm)
    bs.save()
