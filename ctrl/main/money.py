#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from ctrl._urlmap.main import urlmap
from config import SITE_URL
from model.money_alipay import alipay_url_recall

@urlmap('/money/alipay_sync')
class AlipaySync(Base):
    def get(self):
        query = self.request.query
        t = alipay_url_recall(query)
        url = '%s/money' % SITE_URL
        if t:
            if t.id:
                url = "/donate/result/%s"%t.id
            else:
                url = '%s/charged/%s/%s'%(url, t.id, t.to_id)
        return self.redirect(url)
