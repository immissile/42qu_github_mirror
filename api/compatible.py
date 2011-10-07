#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from config import SITE_DOMAIN
from model.zsite import Zsite
from yajl import dumps
from model.user_mail import user_id_by_mail
from model.zsite import Zsite
from model.career import career_current
from model.ico import pic_url
from model.motto import motto_get
from model.zsite_url import url_by_id
from model.zsite_link import name_link_by_zsite_id
from model.txt import txt_get
from zweb.json import jsonp


def _blog_ping(self):
    args = ('id', 'blog_ping', 'blog_link', 'blog_title', 'author', 'mail')

    kw = dict((i, self.get_argument(i, None)) for i in args)

    lack = [k for k, v in kw.iteritems() if v is None]

    #api_blog_new(**kw)

def man_show_api_json(man_id):
    return dumps(man_show_api(man_id))


def man_show_api(man_id):
    man = Zsite.mc_get(man_id)
    if man:
        comp, title = career_current(man_id)
        txt = txt_get(man_id)
        link = man.link
        li = [
            ('id', man_id),
            ('name', man.name),
            ('uid', url_by_id(man_id)),
            ('company', comp),
            ('title', title),
            ('signature', motto_get(man_id)),
            ('about_me', txt),
            ('ico', pic_url(man_id, 219)),
            ('link', name_link_by_zsite_id(man_id, 'http:')),
            ('appearance_fee', 42),
        ]
        return dict(filter(lambda x:bool(x[1]), li))
    return {}


@urlmap('/search/man/(.+)')
@urlmap(r"/man/(\d+)/show")
class ApiMan(_handler.OauthBase):
    def get(self, id):
        if not id.isdigit():
            _blog_ping(self)
            id = user_id_by_mail(id) or 0
        self.finish(
            jsonp(
                self,
                man_show_api_json(int(id))
            )
        )
    post = get


@urlmap(r"/man/blog_bind")
class BlogBind(_handler.OauthBase):
    def get(self):
        _blog_ping(self)

        next = self.get_argument('next', None)
        if next:
            back = self.get_argument('back', None)
            redirect_to = urlparse.urlunsplit(
                (
                    'http',
                    SITE_DOMAIN,
                    urlparse.urlsplit(next).path,
                    urllib.urlencode({'back': back}) if back else '',
                    ''
                )
            )
            return self.redirect(redirect_to)

        self.finish(jsonp(self, '{}'))

    post = get

