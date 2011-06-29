#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import Base
from _urlmap import urlmap

from model.user_mail import user_id_by_mail

@urlmap('/')
class Index(Base):
    def get(self):
        query_id=None
        self.render(
            query_id=query_id,
            mail='',
            )

    def post(self):
        _mail = self.get_argument('mail', None)
        if _mail:
            data = user_id_by_mail(_mail)
            if data:
                query_id = data
            else:
                query_id = None
        
        self.render(
            query_id=query_id,
            mail=_mail,
            )

@urlmap('/chart')
class Chart(Base):
    def get(self):
        self.render()
