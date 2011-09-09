#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap
from zkit.page import page_limit_offset
from model.money import Trade, TRADE_STATE_FINISH

PAGE_LIMIT = 100

@urlmap('/trade_list')
@urlmap('/trade_list-(\d+)')
class TradeList(Base):
    def get(self, n=1):
        total = Trade.where('state=%s', TRADE_STATE_FINISH).count()
        page, limit, offset = page_limit_offset(
            href='/trade_list-%s',
            total=total,
            n=n,
            limit=PAGE_LIMIT
        )
        trade_list = Trade.where('state=%s', TRADE_STATE_FINISH).order_by('id desc')[offset:offset+limit]

        self.render(
            trade_list=trade_list,
            page=page,
        )


