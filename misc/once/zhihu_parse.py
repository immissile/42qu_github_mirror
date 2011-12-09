#!/usr/bin/env python
# -*- coding: utf-8 -*-

import _env
from zkit.bot_txt import txt_wrap_by_all, txt_wrap_by
from zkit.htm2txt import htm2txt
from json import loads, dumps

def page_parse(htm_file):
    html = open(htm_file).read()
    title = txt_wrap_by('<title>', '- 知乎', html)
    tags = txt_wrap_by_all('xgm" href="javascript:;">', '</', html)


