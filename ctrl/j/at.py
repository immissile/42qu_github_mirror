#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yajl import dumps
from ctrl._urlmap.j import urlmap
from model.zsite_url import zsite_by_domain
from _handler import JLoginBase
from model.zsite_url import url_or_id

@urlmap('/j/at/')
class At(JLoginBase):
    def post(self):
        result = []
        result.append(('王大牛','宇宙银行主管','wangdaniu','http://img4.douban.com/icon/u50800918-10.jpg'))
        result.append(('张飞虎','世界联合妓院副总裁','tiger','http://img3.douban.com/icon/u2194922-21.jpg'))
        result.append(('何二狗','斧头帮市场总监,斧爱联合创始人','doghe','http://img3.douban.com/icon/u30288360-57.jpg'))
        result.append(('陈冠希','国际摄影协会秘书长,国际性爱学会理事','edison','http://img3.douban.com/icon/u40915253-14.jpg'))
        self.finish(dumps(result))


