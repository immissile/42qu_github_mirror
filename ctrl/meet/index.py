# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.meet import urlmap
from model.namecard import namecard_get
from zkit.earth import pid_city
@urlmap('/')
class Index(Base):
    def get(self):
        user_id = self.current_user_id
        if not user_id:
            return self.redirect('/guest')
        namecard = namecard_get(user_id)
        location = pid_city(namecard.pid_now)
        if not location:
            return self.redirect('/guest')
        

        return self.render(location = location)
