#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from os.path import dirname, abspath
PWD = dirname(abspath(__file__))
sys.path.append(dirname(dirname(dirname(PWD))))

from zpage import config
config.DISABLE_LOCAL_CACHED = True
