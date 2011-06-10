#!/usr/bin/env python
#coding:utf-8

import _handler
from zweb._urlmap import urlmap
from model.po import Po, po_rm, po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set, CID_NOTE
from model.po_pic import  pic_list, pic_list_edit, mc_pic_id_list
from model import reply
from zkit.jsdict import JsDict

def update_pic(form, user_id, po_id, id):
    pl = pic_list(user_id, id)
    for pic in pl:
        seq = pic.seq
        title = form['tit%s' % seq][0]
        align = form['pos%s' % seq][0]
        pic.title = title.strip()
        align = int(align)

        if align not in (-1, 0, 1):
            align = 0

        pic.align = align
        pic.po_id = po_id
        pic.save()


@urlmap('/po/note')
@urlmap('/note/edit/(\d+)')
class Edit(_handler.LoginBase):
    @staticmethod
    def _can_edit(current_user_id, id):
        if id:
            po = Po.mc_get(id)
            if not po:
                po = None
            if not po.can_admin(current_user_id):
                po = None
        else:
            po = None
        return po or JsDict()

    def get(self, id=0):
        current_user_id = self.current_user_id
        po = self._can_edit(current_user_id, id)
        self.render(po=po, pic_list=pic_list_edit(current_user_id, id))

    def post(self, id=0):
        current_user_id = self.current_user_id
        po = self._can_edit(current_user_id, id)
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        secret = self.get_argument('secret', None)
        arguments = self.request.arguments
        if secret:
            state = STATE_SECRET
        else:
            state = STATE_ACTIVE
        if po:
            if name:
                po.name = name
                po.save()
            if txt:
                po.txt_set(txt)
            po_state_set(po, state)
        else:
            po = po_note_new(current_user_id, name, txt, state)

        if po:
            link = po.link
            update_pic(arguments, current_user_id, po.id, id)
            mc_pic_id_list.delete('%s_%s'%(current_user_id, id))
        else:
            link = '/po/note'
        self.redirect(link)










