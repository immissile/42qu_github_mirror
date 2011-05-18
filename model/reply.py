#!/usr/bin/env python
#coding:utf-8
from gid import gid

class ReplyMixin(object):
    def reply_new(self, user_id, txt):
        rid = self.id
        self.reply_count += 1
        self.save()
        id = gid()
        s = Rcls(id=id, rid=rid, user_id=user_id, state=state)
        s.txt = txt
        s.save()


        return s


def mixin_reply(reply_cls):
    """
@mixin_reply(XxxReply)
class Xxx(McModel):
    pass
    """
    def _(cls):
        cls.__bases__ = tuple(list(cls.__bases__)+[ReplyMixin, ])
        table_title = cls.Meta.table.title()
        cls._REPLY_CLS = reply_cls
        return cls
    return _


