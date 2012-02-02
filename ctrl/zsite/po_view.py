#!/usr/bin/env python
# -*- coding: utf-8 -*-
from _handler import ZsiteBase, LoginBase, XsrfGetBase, login,Base
from ctrl._urlmap.zsite import urlmap
from model.po_prev_next import po_prev_next
from model.zsite_tag import zsite_tag_id_tag_name_by_po_id
from model.po import po_rm, po_word_new, Po, STATE_SECRET, STATE_ACTIVE, po_list_count, po_view_list, CID_QUESTION, PO_EN, PO_SHARE_FAV_CID, reply_rm_if_can
from model.po_question import po_answer_new
from model.po_pos import po_pos_get, po_pos_mark, po_pos_state, STATE_BUZZ, po_pos_state_buzz
from model import reply
from model.zsite import Zsite, user_can_reply
from model.zsite_tag import zsite_tag_list_by_zsite_id, po_id_list_by_zsite_tag_id_cid, zsite_tag_cid_count
from model.cid import CID_REVIEW, CID_WORD, CID_NOTE, CID_QUESTION, CID_ANSWER, CID_PHOTO, CID_REC,\
CID_VIDEO, CID_AUDIO, CID_PO, CID_EVENT, CID_EVENT_FEEDBACK, CID_EVENT_NOTICE, CID_SITE
from zkit.page import page_limit_offset
from zkit.txt import cnenlen
from model.zsite_tag import ZsiteTag , link_by_zsite_id_tag_id
from model.feed_render import feed_tuple_list
from model.tag import Tag
from model.event import Event, EVENT_STATE_TO_REVIEW
from model.fav import fav_user_count_by_po_id, fav_user_list_by_po_id
from model.vote import vote_up_count, vote_user_id_list
from model.site_po import feed_po_list_by_zsite_id, po_cid_count_by_zsite_id, PAGE_LIMIT
from model.buzz_reply import buzz_reply_hide

@urlmap('/po')
class Index(ZsiteBase):
    def get(self):
        self.render()


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

    def get(self, n=1):
        zsite_id = self.zsite_id
        user_id = self.current_user_id
        zsite = self.zsite
        zsite_cid = zsite.cid

        if zsite_cid == CID_SITE:
            self.template = '/ctrl/zsite/po_view/site_po_page.htm'
        else:
            self.template = '/ctrl/zsite/po_view/po_page.htm'


        cid = self.cid
        page_template = self.page_template
        n = int(n)

        if zsite_cid == CID_SITE:
            total = po_cid_count_by_zsite_id(zsite_id, cid)
        else:
            is_self = zsite_id == user_id
            total = po_list_count(zsite_id, cid, is_self)

        page, limit, offset = page_limit_offset(
            page_template,
            total,
            n,
            PAGE_LIMIT
        )

        if n != 1 and offset >= total:
            return self.redirect(page_template[:-3])

        if zsite_cid == CID_SITE:
            po_list = feed_po_list_by_zsite_id(user_id, zsite_id, cid, limit, offset)
            back_a = None
            total = 0
        else:
            po_list = po_view_list(zsite_id, cid, is_self, limit, offset)

            if cid == CID_WORD:
                rid_po_list = [i for i in po_list if i.rid]
                Po.mc_bind(rid_po_list, 'question', 'rid')
                Zsite.mc_bind([i.target for i in rid_po_list], 'user', 'user_id')

            if is_self:
                back_a = '/feed'
            else:
                back_a = '/'


        self.render(
            cid=cid,
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
    template = '/ctrl/zsite/po_view/po_page.htm'

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


PO_TEMPLATE = '/ctrl/zsite/po_view/po.htm'
CID2TEMPLATE = {
    CID_WORD:'/ctrl/zsite/po_view/word.htm',
    CID_REVIEW:'/ctrl/zsite/po_view/word.htm',
    CID_NOTE: PO_TEMPLATE,
    CID_QUESTION:'/ctrl/zsite/po_view/question.htm',
    CID_ANSWER: PO_TEMPLATE,
    CID_EVENT_NOTICE: '/ctrl/zsite/po_view/notice.htm',
    CID_PHOTO: '/ctrl/zsite/po_view/photo.htm',
    CID_VIDEO: '/ctrl/zsite/po_view/video.htm',
    CID_EVENT: '/ctrl/zsite/po_view/event.htm',
    CID_AUDIO: '/ctrl/zsite/po_view/audio.htm',
    CID_EVENT_FEEDBACK: PO_TEMPLATE,
    CID_REC: '/ctrl/zsite/po_view/word.htm',
}


@urlmap('/(\d+)')
class PoOne(Base):
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
            po_pos_state_buzz(user_id, po)

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


        if cid == CID_EVENT:
            zsite_tag_id = tag_name = None
            event = Event.mc_get(id)
            if event.state <= EVENT_STATE_TO_REVIEW:
                tag_link = '/event/to_review'
            else:
                tag_link = '/event'
        elif cid == CID_EVENT_NOTICE:
            zsite_tag_id = tag_name = None
            tag_link = '/%s'%po.rid
        else:
            zsite_tag_id, tag_name = zsite_tag_id_tag_name_by_po_id(po.user_id, id)
            if zsite_tag_id:
                tag_link = '/tag/%s' % zsite_tag_id
            else:
                tag_link = '/po/cid/%s'%cid

        prev_id, next_id = po_prev_next(
            po, zsite_tag_id
        )

        buzz_reply_hide(user_id,po.id)

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
        po_pos_state_buzz(user_id, po)

    def post(self, id):
        user_id = self.current_user_id
        if not user_id:
            return request.redirect('/auth/login')

        question = self.po(id)
        if question is None:
            return

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

@urlmap('/tag')
class TagIndex(ZsiteBase):
    def get(self):
        return self.render()

@urlmap('/tag-(\d+)')
class TagRedirect(ZsiteBase):
    def get(self, id):
        zsite_id = self.zsite_id
        link = link_by_zsite_id_tag_id(zsite_id, id)
        return self.redirect(link)

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


@urlmap('/po/rm/reply/(\d+)')
class ReplyRm(LoginBase):
    def post(self, id):
        user_id = self.current_user_id
        self.finish({'success': reply_rm_if_can(user_id, id)})


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
        self.redirect('%s/feed'%user.link)

    post = get


class ShareFavBase(ZsiteBase):
    template = '/ctrl/zsite/po_view/zsite_list.htm'

    def po(self, id):
        po = Po.mc_get(id)
        if po:
            if po.cid in PO_SHARE_FAV_CID and po.can_view(self.current_user_id):
                if po.user_id == self.zsite_id:
                    return po
                return self.redirect('%s%s' % (po.user.link, self.request.path))
            return self.redirect(po.link)
        return self.redirect('/')


@urlmap('/(\d+)/share')
@urlmap('/(\d+)/share-(\d+)')
class PoShare(ShareFavBase):
    def get(self, id, n=1):
        po = self.po(id)
        if po is None:
            return

        path = '/%s/fav' % id

        total = vote_up_count(id)
        page, limit, offset = page_limit_offset(
            '%s-%%s' % path,
            total,
            n,
            PAGE_LIMIT
        )
        if type(n) == str and offset >= total:
            return self.redirect(path)

        id_list = vote_user_id_list(id, limit, offset)
        zsite_list = Zsite.mc_get_list(id_list)

        self.render(
            po=po,
            zsite_list=zsite_list,
            page=page,
            title='分享',
            path=path,
        )


@urlmap('/(\d+)/fav')
@urlmap('/(\d+)/fav-(\d+)')
class PoFav(ShareFavBase):
    def get(self, id, n=1):
        po = self.po(id)
        if po is None:
            return

        path = '/%s/fav' % id

        total = fav_user_count_by_po_id(id)
        page, limit, offset = page_limit_offset(
            '%s-%%s' % path,
            total,
            n,
            PAGE_LIMIT
        )
        if type(n) == str and offset >= total:
            return self.redirect(path)

        zsite_list = fav_user_list_by_po_id(id, limit, offset)

        self.render(
            po=po,
            zsite_list=zsite_list,
            page=page,
            title='收藏',
            path=path,
        )


#@urlmap('/tag')
#class GlobalTag(ZsiteBase):
#    def get(self):
#        tag_list = zsite_tag_list_by_zsite_id(self.zsite_id)
#        self.render(
#        tag_list=tag_list,
#        )
