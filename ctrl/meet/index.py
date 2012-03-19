# -*- coding: utf-8 -*-
from _handler import Base, LoginBase
from ctrl._urlmap.meet import urlmap
from model.namecard import namecard_get
from zkit.earth import pid_city
from model.event import event_list_by_city_pid_cid, event_count_by_city_pid_cid, event_end_list_by_city_pid, event_end_count_by_city_pid, EVENT_STATE_END
from zkit.jsdict import JsDict
from zkit.page import page_limit_offset
from model.namecard import namecard_get, namecard_new

PAGE_LIMIT = 25

@urlmap('/')
class Index(Base):
    def get(self):
        user_id = self.current_user_id

        if user_id:
            link = '/city/set'
            namecard = namecard_get(user_id)
            if namecard:
                pid_now = namecard.pid_now
                if pid_now:
                    pid = pid_city(pid_now)
                    if pid:
                        link = '/%s'%pid
        else:
            link = '/city/select'

        return self.redirect(link)


@urlmap('/(?P<pid>\d+)')
@urlmap('/(?P<pid>\d+)-(?P<n>\d+)')
@urlmap('/(?P<pid>\d+)/(?P<cid>\d+)')
@urlmap('/(?P<pid>\d+)/(?P<cid>\d+)-(?P<n>\d+)')
class City(Base):
    def get(self, pid, cid=0, n=1):
        pid = int(pid)
        cid = int(cid)

        _pid = pid_city(pid)
        if not _pid:
            return self.redirect('/')
        if _pid != pid:
            return self.redirect('/%s'%_pid)

        if cid:
            page_template = '/%s/%s-%%s' % (pid, cid)
        else:
            page_template = '/%s-%%s' % pid
        total = event_count_by_city_pid_cid(pid, cid)
        page, limit, offset = page_limit_offset(
            page_template,
            total,
            n,
            PAGE_LIMIT,
        )
        event_list = event_list_by_city_pid_cid(pid, cid, limit, offset)
        return self.render(
            pid=pid,
            cid=cid,
            event_list=event_list,
            page=page,
        )


@urlmap('/(\d+)/ago')
@urlmap('/(\d+)/ago-(\d+)')
class CityAgo(Base):
    def get(self, pid, n=1):
        pid = int(pid)
        _pid = pid_city(pid)
        if not _pid:
            return self.redirect('/')
        if _pid != pid:
            return self.redirect('/%s' % _pid)

        total = event_end_count_by_city_pid(pid)
        page, limit, offset = page_limit_offset(
            '/%s/ago-%%s' % pid,
            total,
            n,
            PAGE_LIMIT,
        )
        event_list = event_end_list_by_city_pid(pid, limit, offset)
        return self.render(
            'ctrl/meet/index/city.htm',
            pid=pid,
            state=EVENT_STATE_END,
            event_list=event_list,
            page=page,
        )


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
        pid_now = self.get_argument('pid_now', '1')
        pid_now = int(pid_now)
        if pid_city(pid_now):
            namecard_new(current_user_id, pid_now)
            self.redirect('/%s'%pid_now)
        else:
            self.render(pid_now=pid_now or 0, error='请选择现居城市')

