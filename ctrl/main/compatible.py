# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.main import urlmap
from config import SITE_DOMAIN

@urlmap('/-(\d+)/pay')
class Index(Base):
    def get(self, name):
        url = '//%s.%s/pay'%(name, SITE_DOMAIN)
        query = self.request.query
        if query:
            url = '%s?%s' % (url, query)
        #import pdb;pdb.set_trace()
        return self.redirect(url, True)

    post = get
