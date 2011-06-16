# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.me import urlmap
from model.po import Po, po_rm, po_word_new, po_note_new, STATE_SECRET, STATE_ACTIVE, po_state_set
from model.po_question import po_question_new, po_answer_new
from model.po_pic import pic_list, pic_list_edit, mc_pic_id_list
from model.po_pos import po_pos_get, po_pos_set
from model import reply
from model.zsite import Zsite
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


@urlmap('/po/(\d+)')
class PoIndex(Base):
    def get(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        if po:
            link = po.link
            pos, state = po_pos_get(current_user_id, id)
            if pos > 0:
                link = '%s#reply%s' % (link, pos)
        else:
            link = '/'
        self.redirect(link)


@urlmap('/po/word')
class Word(LoginBase):
    def post(self):
        current_user = self.current_user
        txt = self.get_argument('txt', '')
        if txt.strip():
            po_word_new(current_user.id, txt)
        return self.redirect('/live')


def po_can_edit(current_user_id, id):
    if id:
        po = Po.mc_get(id)
        if po:
            if po.can_admin(current_user_id):
                return po
    return JsDict()

@urlmap("/po/edit/(\d+)")
class Edit(LoginBase):
    def get(self, id=0):
        self.redirect("/note/edit/%s"%id)


@urlmap('/po/note')
@urlmap('/note/edit/(\d+)')
class Note(LoginBase):
    def get(self, id=0):
        current_user_id = self.current_user_id
        po = po_can_edit(current_user_id, id)
        self.render(po=po, pic_list=pic_list_edit(current_user_id, id))

    def post(self, id=0):
        current_user_id = self.current_user_id
        po = po_can_edit(current_user_id, id)
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        if not (name or txt):
            return self.get(id)
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
            po_id = po.id
            link = '/po/tag/%s'%po_id
            zsite_tag_new_by_tag_id(po)
            update_pic(arguments, current_user_id, po_id, id)
            mc_pic_id_list.delete('%s_%s'%(current_user_id, id))
        else:
            link = '/po/note'
        self.redirect(link)


@urlmap('/po/question')
@urlmap('/question/edit/(\d+)')
class Question(LoginBase):
    def get(self, id=0):
        current_user_id = self.current_user_id
        po = po_can_edit(current_user_id, id)
        self.render(po=po, pic_list=pic_list_edit(current_user_id, id))

    def post(self, id=0):
        current_user_id = self.current_user_id
        po = po_can_edit(current_user_id, id)
        name = self.get_argument('name', '')
        txt = self.get_argument('txt', '')
        arguments = self.request.arguments
        if po:
            if name:
                po.name = name
                po.save()
            if txt:
                po.txt_set(txt)
        else:
            po = po_question_new(current_user_id, name, txt)

        if po:
            link = po.link
            update_pic(arguments, current_user_id, po.id, id)
            mc_pic_id_list.delete('%s_%s'%(current_user_id, id))
        else:
            link = '/po/question'
        self.redirect(link)


from model.zsite_tag import zsite_tag_list_by_zsite_id_with_init, tag_id_by_po_id,\
zsite_tag_new_by_tag_id, zsite_tag_new_by_tag_name


@urlmap('/po/tag/(\d+)')
class Tag(LoginBase):
    def _po(self, id):
        current_user = self.current_user
        current_user_id = self.current_user_id
        po = Po.mc_get(id)
        if not po:
            self.redirect('/')
            return
        if not po.can_admin(current_user_id):
            self.redirect(po.link)
            return
        return po

    def get(self, id):
        po = self._po(id)
        if po:
            current_user_id = self.current_user_id
            tag_list = zsite_tag_list_by_zsite_id_with_init(current_user_id)
            po_id = po.id
            tag_id = tag_id_by_po_id(current_user_id, po_id) or 1
            self.render(tag_list=tag_list, po=po, tag_id=tag_id)

    def post(self, id):
        po = self._po(id)
        if po:
            tag_id = int(self.get_argument('tag'))
            name = self.get_argument('name',None)
            if not name and not tag_id:
                tag_id = 1

            if tag_id:
                zsite_tag_new_by_tag_id(po, tag_id)
            else:
                zsite_tag_new_by_tag_name(po, name)

            self.redirect(po.link)
