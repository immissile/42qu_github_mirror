# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.meet import urlmap
from model.namecard import namecard_get
from zkit.earth import pid_city
from model.event import event_list_by_city_pid
from zkit.jsdict import JsDict
from model.namecard import namecard_get, namecard_new


@urlmap('/')
@urlmap('/(\d+)')
class Index(Base):
    def get(self,location=0):
        location = int(location)
        user_id = self.current_user_id
        if not location:
            if not user_id:
                return self.redirect('/city_select')
            namecard = namecard_get(user_id)
            if namecard.pid_now:
                location = pid_city(namecard.pid_now)
                if not location:
                    return self.redirect('/city_set')
        event_list = event_list_by_city_pid(location)
        return self.render(location = location, event_list = event_list)

@urlmap('/city_select')
class CitySelect(Base):
    def get(self):
        self.render()

@urlmap('/city_set')
class CitySet(LoginBase):
    def get(self):
        current_user_id = self.current_user_id
        c = namecard_get(current_user_id) or JsDict()
        self.render(pid_now=c.pid_now or 0)
    
    def post(self):
        current_user_id = self.current_user_id
        pid_now = self.get_argument('pid_now','1')
        pid_now = int(pid_now)
        c = namecard_new(
                    current_user_id,pid_now
                    )
        if pid_city(pid_now):
            self.redirect('/')
        else:
            self.render(pid_now=pid_now or 0, message="请确认！")
