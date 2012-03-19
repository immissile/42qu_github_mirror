# -*- coding: utf-8 -*-
from _handler import Base, LoginBase
from ctrl._urlmap.main import urlmap
from model.zsite_tag import ZsiteTag
from model.zsite import Zsite
from model.oauth import oauth_by_zsite_id_last
from model.sync import sync_follow_oauth_id_bind

@urlmap('/')
class Index(Base):
    def get(self):
        current_user = self.current_user
        if current_user:
            self.redirect(
                '%s/feed'%current_user.link
            )
        else:
            self.redirect('/login')


@urlmap('/tag/(\d+)')
class Tag(Base):
    def get(self, id, n=1):
        tag = ZsiteTag.mc_get(id)
        tag_zsite = Zsite.mc_get(tag.zsite_id)
        return self.redirect('%s/tag/%s'%(tag_zsite.link, id))



@urlmap('/i/mail_notice')
@urlmap('/i/mail/notice')
class MailNotice(LoginBase):
    def get(self):
        return self.redirect('//%s/i/mail/notice'%self.current_user.link)


@urlmap('/i/bind')
class Bind(LoginBase):
    def get(self):
        user = self.current_user
        link = user.link

        oauth_id = oauth_by_zsite_id_last(user.id)
        if oauth_id:
            link = '%s/i/bind/%s'%(link, oauth_id[1])
            sync_follow_oauth_id_bind(
                user.id, oauth_id[0], oauth_id[1]
            )

        return self.redirect(link)


