# -*- coding: utf-8 -*-
import model._db
from zweb._handler import Base as _Base

class Base(_Base):
    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)


class JLoginBase(Base):
    def prepare(self):
        super(JLoginBase, self).prepare()
        if not self.current_user:
            self.finish('{"login":1}')

