#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from ctrl._urlmap.main import urlmap
from config import SITE_URL
from model.money_alipay import alipay_url_recall
from model.money import pay_new, TRADE_STATE_ONWAY, TRADE_STATE_FINISH, pay_account_get, bank, Trade, trade_log, pay_notice
from model.zsite import Zsite
from model.cid import CID_TRADE_CHARDE, CID_TRADE_WITHDRAW, CID_TRADE_DEAL, CID_TRADE_EVENT
from model.zsite import Zsite
from model.money import Trade
from model.po import Po
from model.event import Event


@urlmap('/money/alipay_sync')
class AlipaySync(Base):
    def get(self):
        query = self.request.query
        t = alipay_url_recall(query)

        if t.for_id:
            t = Trade.get(t.for_id)

        url = SITE_URL

        if t:
            cid = t.cid
            if cid == CID_TRADE_CHARDE:
                user = Zsite.mc_get(t.to_id)
                url = '%s/money/charged/%s/%s'%(user.link, t.id, t.to_id)
            elif cid == CID_TRADE_EVENT:
                event = Event.mc_get(t.rid)
                zsite = Zsite.mc_get(event.zsite_id)
                url = '%s/event/%s/state'%(zsite.link, event.id)
            else:
                url = '/pay/result/%s'%t.id

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



