# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.meet import urlmap

@urlmap('/')
class Index(Base):
    def get(self):
        user_id = self.current_user_id
        if not user_id:
            self.redirect('/guest')
        return self.render()
