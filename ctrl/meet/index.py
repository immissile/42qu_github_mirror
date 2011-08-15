# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.meet import urlmap
from model.namecard import namecard_get
from zkit.earth import pid_city
from model.event import event_list_by_city_pid, event_count_by_city_pid
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from model.namecard import namecard_get, namecard_new

PAGE_LIMIT = 42

@urlmap('/')
class Index(Base):
    def get(self):
        user_id = self.current_user_id

        if user_id:
            link = "/city/set"
            namecard = namecard_get(user_id)
            pid_now = namecard.pid_now
            if pid_now and pid_city(pid_now):
                link = "/%s"%pid_now
        else:
            link = '/city/select'

        return self.redirect(link)


@urlmap('/(\d+)')
@urlmap('/(\d+)-(\d+)')
class City(Base):
    def get(self, pid, n=1):
        pid = int(pid)
        n = int(n)

        if not pid_city(pid):
            return self.redirect("/")

        total = event_count_by_city_pid(pid)
        page, limit, offset = page_limit_offset(
            '%%s-%s' % pid,
            total,
            n,
            PAGE_LIMIT,
        )
        event_list = event_list_by_city_pid(pid, limit, offset)
        return self.render(pid = pid, event_list = event_list, page=page)



@urlmap('/city/select')
class CitySelect(Base):
    def get(self):
        self.render()


@urlmap('/city/set')
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
                current_user_id,
                pid_now
            )
        if pid_city(pid_now):
            self.redirect('/%s'%pid_now)
        else:
            self.render(pid_now=pid_now or 0, error="请选择城市")

