#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _db import Model, McModel

class GoogleRank(Model):
    pass


if __name__ == '__main__':
    from urllib2 import urlopen
    url = 'https://plus.google.com/%s?hl=zh-CN'
    id = 115113322964276305188
    html = urlopen(url%id).read()
    from zkit.bot_txt import txt_wrap_by
    follower = txt_wrap_by(
        '（', '）</h4>', html
    )
    print follower
