# -*- coding: utf-8 -*-
import model._db
from model.zsite_url import zsite_by_domain, url_by_digit_domain
from zweb._handler import Base as _Base

class Base(_Base):
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class JLoginBase(Base):
    def prepare(self):
        super(JLoginBase, self).prepare()
        if not self.current_user:
            self.finish('{"login":1}')

class JLoginZsiteBase(JLoginBase):
    def prepare(self):
        super(JLoginBase, self).prepare()

        request = self.request
        host = request.host
        zsite = zsite_by_domain(host)
        if zsite is None:
            self.zsite_id = 0
        else:
            self.zsite_id = zsite.id
        self.zsite = zsite

        zsite = self.zsite


