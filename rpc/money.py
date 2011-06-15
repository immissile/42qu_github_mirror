#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from config import SITE_URL
from model.money_alipay import alipay_url_recall

@urlmap('/money/alipay_async')
class AlipayAsync(Base):
    def post(self):
        data = self.request.body
        alipay_url_recall(data)
        self.finish('success')

@urlmap('/money/alipay_sync')
class AlipaySync(Base):
    def get(self):
        query = self.request.query
        t = alipay_url_recall(query)
        url = '%s/money' % SITE_URL
        if t:
            url = '%s/charged/%s/%s'%(url, t.id, t.to_id)
        return self.redirect(url)
