#!/usr/bin/env python
# -*- coding: utf-8 

from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from model.po import Po
from model.buzz_reply import buzz_reply_hide_or_rm, buzz_reply_hide_or_rm_by_user_id
from model.buzz_at import buzz_at_hide

@urlmap('/j/buzz/reply/x')
class BuzzX(JLoginBase):
    def post(self):
        current_user_id = self.current_user_id
        buzz_reply_hide_or_rm_by_user_id(current_user_id)
        self.finish('{}')

@urlmap("/j/buzz/at/x")
class BuzzAtX(JLoginBase):
    def post(self):
        current_user_id = self.current_user_id
        buzz_at_hide(current_user_id)
        self.finish('{}')

@urlmap("/j/buzz/at/x/(\d+)")
class BuzzAtX(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        buzz_at_hide(current_user_id, id)
        self.finish('{}')

@urlmap("/j/buzz/reply/x/(\d+)")
class BuzzReplyX(JLoginBase):
    def post(self, id):
        current_user_id = self.current_user_id
        buzz_reply_hide_or_rm(id, current_user_id)
        self.finish('{}')
