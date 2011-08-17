#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from ctrl._urlmap.main import urlmap
from config import SITE_URL
from model.money_alipay import alipay_url_recall
from model.money import pay_new, TRADE_STATE_NEW, TRADE_STATE_ONWAY, TRADE_STATE_FINISH, pay_account_get, bank, Trade, trade_log, pay_notice

@urlmap('/money/alipay_sync')
class AlipaySync(Base):
    def get(self):
        query = self.request.query
        t = alipay_url_recall(query)
        url = '%s/money' % SITE_URL
        if t.id:
            url = '/pay/result/%s'%t.id
        else:
            url = '%s/charged/%s/%s'%(url, t.id, t.to_id)
        return self.redirect(url)


@urlmap('/pay/result/(\d+)')
class Result(Base):
    def get(self, id):
        t = Trade.get(id)
        from_user = Zsite.mc_get(t.from_id)
        to_user = Zsite.mc_get(t.to_id)

        self.render(
            from_user=from_user,
            to_user=to_user,
            trade=t,
        )
