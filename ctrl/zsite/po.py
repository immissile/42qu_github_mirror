#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login
from ctrl._urlmap.zsite import urlmap
from model.po_prev_next import po_prev_next
from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
from model.po import po_rm, po_word_new, Po, STATE_SECRET, STATE_ACTIVE, po_list_count, po_view_list, CID_QUESTION, PO_EN
from model.po_question import po_answer_new
from model.po_pos import po_pos_get, po_pos_set, po_pos_state, STATE_BUZZ
from model import reply
from model.zsite import Zsite, user_can_reply
from model.zsite_tag import zsite_tag_list_by_zsite_id, po_id_list_by_zsite_tag_id_cid, zsite_tag_cid_count
from model.cid import CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_VIDEO, CID_AUDIO, CID_PO, CID_EVENT, CID_EVENT_FEEDBACK, CID_EVENT_NOTICE
from zkit.page import page_limit_offset
from zkit.txt import cnenlen
from model.zsite_tag import ZsiteTag
from model.feed_render import feed_tuple_list
from model.tag import Tag
from model.event import Event, EVENT_STATE_TO_REVIEW

PAGE_LIMIT = 42

@urlmap('/po/cid/(\d+)')
class PoCid(ZsiteBase):
    def get(self, cid):
        cid = int(cid)
        if cid in PO_EN:
            link = '/%s'%PO_EN[cid]
        else:
            link = '/'
        return self.redirect(link)

@urlmap('/po/(\d+)')
class PoIndex(ZsiteBase):
    def get(self, id):
        po = Po.mc_get(id)
        current_user_id = self.current_user_id
        if po:
            link = po.link_reply
            pos, state = po_pos_get(current_user_id, id)
            if pos > 0:
                link = '%s#reply%s' % (link, pos)
        else:
            link = '/'
        self.redirect(link)


class PoPage(ZsiteBase):
    cid = 0
    template = '/ctrl/zsite/po/po_page.htm'

    def get(self, n=1):
        zsite_id = self.zsite_id
        user_id = self.current_user_id
        cid = self.cid
        page_template = self.page_template
        is_self = zsite_id == user_id
        total = po_list_count(zsite_id, cid, is_self)
        n = int(n)

        page, limit, offset = page_limit_offset(
            page_template,
            total,
            n,
            PAGE_LIMIT
        )

        if n != 1 and offset >= total:
            return self.redirect(page_template[:-3])

        po_list = po_view_list(zsite_id, cid, is_self, limit, offset)

        if cid == CID_WORD:
            rid_po_list = [i for i in po_list if i.rid]
            Po.mc_bind(rid_po_list, 'question', 'rid')
            Zsite.mc_bind([i.target for i in rid_po_list], 'user', 'user_id')

        if zsite_id == user_id:
            back_a = '/live'
        else:
            back_a = '/'


        self.render(
            cid=cid,
            is_self=is_self,
            total=total,
            li=po_list,
            page=page,
            back_a=back_a,
        )


@urlmap('/word')
@urlmap('/word-(\d+)')
class WordPage(PoPage):
    cid = CID_WORD
    page_template = '/word-%s'


@urlmap('/note')
@urlmap('/note-(\d+)')
class NotePage(PoPage):
    cid = CID_NOTE
    page_template = '/note-%s'


@urlmap('/question')
@urlmap('/question-(\d+)')
class QuestionPage(PoPage):
    cid = CID_QUESTION
    page_template = '/question-%s'


@urlmap('/photo')
@urlmap('/photo-(\d+)')
class PhotoPage(PoPage):
    cid = CID_PHOTO
    page_template = '/photo-%s'


@urlmap('/video')
@urlmap('/video-(\d+)')
class VideoPage(PoPage):
    cid = CID_VIDEO
    page_template = '/video-%s'


@urlmap('/audio')
@urlmap('/audio-(\d+)')
class AudioPage(PoPage):
    cid = CID_AUDIO
    page_template = '/audio-%s'


@urlmap('/answer')
@urlmap('/answer-(\d+)')
class AnswerPage(PoPage):
    cid = CID_ANSWER
    page_template = '/answer-%s'


class TagPoPage(ZsiteBase):
    cid = 0
    template = '/ctrl/zsite/po/po_page.htm'

    def get(self, zsite_tag_id, n=1):
        tag = ZsiteTag.mc_get(zsite_tag_id)
        zsite_id = self.zsite_id
        user_id = self.current_user_id
        cid = self.cid
        is_self = zsite_id == user_id
        n = int(n)
        total = zsite_tag_cid_count(zsite_tag_id, cid)
        page, limit, offset = page_limit_offset(
            '/tag/%s'%zsite_tag_id + self.page_template,
            total,
            n,
            PAGE_LIMIT
        )

        if n != 1 and offset >= total:
            return self.redirect(self.page_template[:-3])

        po_list = Po.mc_get_list(po_id_list_by_zsite_tag_id_cid(zsite_tag_id, cid, limit, offset))
        self.render(
            cid=cid,
            is_self=is_self,
            total=total,
            li=po_list,
            page=page,
            tag_name=Tag.get(tag.tag_id),
            back_a='/tag/%s'%zsite_tag_id
        )


@urlmap('/tag/(\d+)/note')
@urlmap('/tag/(\d+)/note-(\d+)')
class NotePage(TagPoPage):
    cid = CID_NOTE
    page_template = '/note-%s'


@urlmap('/tag/(\d+)/question')
@urlmap('/tag/(\d+)/question-(\d+)')
class QuestionPage(TagPoPage):
    cid = CID_QUESTION
    page_template = '/question-%s'


@urlmap('/tag/(\d+)/photo')
@urlmap('/tag/(\d+)/photo-(\d+)')
class PhotoPage(TagPoPage):
    cid = CID_PHOTO
    page_template = '/photo-%s'


@urlmap('/tag/(\d+)/video')
@urlmap('/tag/(\d+)/video-(\d+)')
class VideoPage(TagPoPage):
    cid = CID_VIDEO
    page_template = '/video-%s'


@urlmap('/tag/(\d+)/audio')
@urlmap('/tag/(\d+)/audio-(\d+)')
class AudioPage(TagPoPage):
    cid = CID_AUDIO
    page_template = '/audio-%s'


PO_TEMPLATE = '/ctrl/zsite/po/po.htm'
CID2TEMPLATE = {
    CID_WORD:'/ctrl/zsite/po/word.htm',
    CID_NOTE: PO_TEMPLATE,
    CID_QUESTION:'/ctrl/zsite/po/question.htm',
    CID_ANSWER: PO_TEMPLATE,
    CID_EVENT_NOTICE: '/ctrl/zsite/po/notice.htm',
    CID_PHOTO: '/ctrl/zsite/po/photo.htm',
    CID_VIDEO: '/ctrl/zsite/po/video.htm',
    CID_EVENT: '/ctrl/zsite/po/event.htm',
    CID_AUDIO: '/ctrl/zsite/po/audio.htm',
    CID_EVENT_FEEDBACK: PO_TEMPLATE,
}


@urlmap('/(\d+)')
class PoOne(ZsiteBase):
    def po(self, id):
        po = Po.mc_get(id)
        if po:
            self._po = po
            if po.user_id == self.zsite_id:
                return po
            return self.redirect(po.link)
        return self.redirect('/')

    @property
    def template(self):
        return CID2TEMPLATE[self._po.cid]

    def mark(self):
        po = self._po
        user_id = self.current_user_id
        cid = po.cid
        if cid != CID_QUESTION:
            po_pos_set(user_id, po)
            po_pos_state(user_id, po.id, STATE_BUZZ)

    def get(self, id):
        po = self.po(id)
        if po is None:
            return

        zsite_id = self.zsite_id
        user_id = self.current_user_id
        can_admin = po.can_admin(user_id)
        can_view = po.can_view(user_id)

        if can_view and user_id:
            self.mark()

        cid = po.cid

        prev_id = next_id = None

        if cid == CID_EVENT:
            prev_id = next_id = zsite_tag_id = tag_name = None
            event = Event.mc_get(id)
            if event.state <= EVENT_STATE_TO_REVIEW:
                tag_link = "/event/to_review"
            else:
                tag_link = "/event"
        elif cid == CID_EVENT_NOTICE:
            prev_id = next_id = zsite_tag_id = tag_name = None
            tag_link = "/%s"%po.rid
        else:
            zsite_tag_id, tag_name = zsite_tag_id_tag_name_by_po_id(po.user_id, id)
            if zsite_tag_id:
                prev_id, next_id = po_prev_next(
                    cid, zsite_id, zsite_tag_id, po.id
                )
                tag_link = "/tag/%s" % zsite_tag_id
            else:
                tag_link = "/po/cid/%s"%cid

        return self.render(
            self.template,
            po=po,
            can_admin=can_admin,
            can_view=can_view,
            zsite_tag_id=zsite_tag_id,
            prev_id=prev_id,
            next_id=next_id,
            tag_name=tag_name,
            tag_link=tag_link
        )


@urlmap('/question/(\d+)')
class Question(PoOne):
    template = PO_TEMPLATE

    def mark(self):
        po = self._po
        user_id = self.current_user_id
        po_pos_set(user_id, po)
        po_pos_state(user_id, po.id, STATE_BUZZ)

    def post(self, id):
        question = self.po(id)
        if question is None:
            return

        user_id = self.current_user_id
        txt = self.get_argument('txt', '')
        if not question.can_view(user_id) or not txt:
            return self.get(id)

        secret = self.get_argument('secret', None)
        arguments = self.request.arguments
        if secret:
            state = STATE_SECRET
        else:
            state = STATE_ACTIVE

        if cnenlen(txt) > 140:
            name = ''
        else:
            name, txt = txt, ''
        po = po_answer_new(user_id, id, name, txt, state)

        if po:
            if po.cid == CID_ANSWER and po.state == STATE_ACTIVE:
                answer_id = po.id
                link = '/po/tag/%s' % answer_id
            else:
                link = '%s#reply%s' % (question.link, po.id)
        else:
            link = '%s#reply_txt' % question.link
        self.redirect(link)


@urlmap('/tag/(\d+)')
class PoTag(ZsiteBase):
    def get(self, id, n=1):
        tag = ZsiteTag.mc_get(id)

        if tag is None:
            return self.redirect('/')

        if tag.zsite_id != self.zsite_id:
            tag_zsite = Zsite.mc_get(tag.zsite_id)
            return self.redirect('%s/tag/%s'%(tag_zsite.link, id))

        self.render(
            tag_name=Tag.get(tag.tag_id),
            zsite_tag_id=id
        )


@urlmap('/po/reply/rm/(\d+)')
class ReplyRm(LoginBase):
    def post(self, id):
        user_id = self.current_user_id
        r = reply.Reply.mc_get(id)

        if r:
            po = Po.mc_get(r.rid)
            if po:
                can_rm = r.can_rm(user_id) or po.can_admin(user_id)
                if can_rm:
                    r.rm()

        self.finish({'success': can_rm})


@urlmap('/po/reply/(\d+)')
class Reply(LoginBase):
    def post(self, id):
        po = Po.mc_get(id)
        link = '/'
        if po:
            user = self.current_user
            if user_can_reply(user):
                user_id = self.current_user_id
                can_view = po.can_view(user_id)
                link = po.link_reply
                if can_view:
                    txt = self.get_argument('txt', '')
                    m = po.reply_new(user, txt, po.state)
                    if m:
                        link = '%s#reply%s' % (link, m)
        self.redirect(link)

    def get(self, id):
        po = Po.mc_get(id)
        if po:
            link = po.link
        else:
            link = '/'
        self.redirect(link)


@urlmap('/po/rm/(\d+)')
class Rm(XsrfGetBase):
    def get(self, id):
        user = self.current_user
        user_id = self.current_user_id
        po_rm(user_id, id)
        self.redirect('%s/live'%user.link)

    post = get


#@urlmap('/tag')
#class GlobalTag(ZsiteBase):
#    def get(self):
#        tag_list = zsite_tag_list_by_zsite_id(self.zsite_id)
#        self.render(
#        tag_list=tag_list,
#        )
