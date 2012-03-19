# -*- coding: utf-8 -*-
from _handler import Base
from ctrl._urlmap.main import urlmap
from config import SITE_DOMAIN



@urlmap('/-(\d+)/pay')
@urlmap('/(\w+)/pay')
class Pay(Base):
    def get(self, name):
        url = '//%s.%s/pay'%(name, SITE_DOMAIN)
        query = self.request.query
        if query:
            url = '%s?%s' % (url, query)
        return self.redirect(url, True)

    post = get



@urlmap('/-(\d+)')
class Index(Base):
    def get(self, id):
        return self.redirect('//%s.%s'%(id, SITE_DOMAIN), True)


