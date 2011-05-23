#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.mblog import Mblog, mblog_note_can_view
from model.zsite import Zsite


@urlmap("/note/(\d+)")
class Note(_handler.Base):
    def get(self, id):
        mblog = Mblog.get(id)
        current_user_id = self.current_user_id
        if mblog.user_id != self.zsite_id:
            zsite = Zsite.mc_get(mblog.user_id)
            return self.redirect(
                "%s/note/%s"%(
                    zsite.link,
                    id
                ), True
            )
        can_view = mblog_note_can_view(mblog, current_user_id)
        return self.render(
            mblog=mblog,
            can_view=can_view
        )


@urlmap("/note/(\d+)/rm")
class NoteRm(_handler.XsrfGetBase):
    def get(self, id):
        pass

    post = get


@urlmap("/note/(\d+)/edit")
class NoteEdit(_handler.XsrfGetBase):
    def get(self, id):
        pass

    def post(self, id):
        pass







