# -*- coding: utf-8 -*-
from ctrl.me._handler import Base


class JLoginBase(Base):
    def prepare(self):
        super(JLoginBase, self).prepare()
        if not self.current_user:
            self.finish('{"login":1}')

    def post(self, *args, **kwargs):
        return self.get(*args, **kwargs)
