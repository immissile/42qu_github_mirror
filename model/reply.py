#!/usr/bin/env python
#coding:utf-8
from gid import gid

class ReplyMixin(object):
    def reply_new(self, user_id, txt):
      #  rid = self.id
      #  id = gid()
      #  s = Rcls(id=id, rid=rid, user_id=user_id, state=state)
      #  s.txt = txt
      #  s.save()
        print self.Meta.table
        return s


