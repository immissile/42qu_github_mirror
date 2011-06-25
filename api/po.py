#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.po import po_word_new, Po, po_rm
from model.zsite import user_can_reply, Zsite
from model import reply



@urlmap('/po/word')
class PoWord(_handler.ApiLoginBase):
    def get(self):
        user_id = self.current_user_id
        txt = self.get_argument('txt')
        result = {}
        if txt.strip():
            m = po_word_new(user_id, txt)
            if m:
                result['id'] = m.id
                result['link'] = 'http:%s'%m.link
        self.finish(result)


@urlmap('/po')
class PoAll(_handler.ApiLoginBase):
    def get(self):
        user_id = self.current_user_id
        po_id = int(self.get_argument('iterm_id'))
        po = Po.mc_get(po_id)
        itr = []
        if po.user_id == user_id:
            for reply in po.reply_list():
                re = {}
                re['id'] = reply.id
                re['user_id'] = reply.user.id
                re['user_name'] = reply.user.name
                re['txt'] = reply.txt
                re['timestamp'] = reply.create_time
                itr.append(re)
        self.finish({
                'iterm':itr    
            })


@urlmap('/po/rm')
class PoRm(_handler.ApiLoginBase):
    def get(self):
        id = int(self.get_argument('po_id'))
        user = self.current_user
        user_id = self.current_user_id
        m = po_rm(user_id, id)
        self.finish({
                'status':m
            })

        
@urlmap('/po/reply')
class PoReply(_handler.ApiLoginBase):
    def get(self):
        id = int(self.get_argument('po_id'))
        po = Po.mc_get(id)
        if po:
            user = self.current_user
            if user_can_reply(user):
                user_id = self.current_user_id
                can_view = po.can_view(user_id)
                link = po.link_reply
                if can_view:
                    txt = self.get_argument('txt', '')
                    m = po.reply_new(user, txt, po.state)
        self.finish({
                'id' : m
            })


@urlmap('/po/reply/rm')
class PoReplyRm(_handler.ApiLoginBase):
    def get(self):
        id = int(self.get_argument('po_id'))
        user_id = self.current_user_id
        r = reply.Reply.mc_get(id)

        if r:
            po = Po.mc_get(r.rid)
            if po:
                can_rm = r.can_rm(user_id) or po.can_admin(user_id)
                if can_rm:
                    r.rm()

        self.finish({'status': can_rm})


