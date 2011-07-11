# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.hero import urlmap
from string import maketrans
from urllib import quote
from urlparse import parse_qs
from model.search import search
from model.zsite import Zsite
from zkit.page import limit_offset, Page

PAGE_LIMIT = 64
SAFE_TABLE = maketrans('/,. ', '++++')

@urlmap('/q')
@urlmap('/q/(?P<q>[^/]+)')
@urlmap('/q-(\d+)/([^/]+)')
class Search(Base):
    def get(self, n=1, q=''):
        if not q:
            if 'q' in self.request.query:
                link = '/q'
                q = self.get_argument('q', '')
                q = q.lower().translate(SAFE_TABLE)
                if q:
                    link = '%s/%s' % (link, quote(q))
                return self.redirect(link)
            else:
                self.render(
                    q = None,
                )
        if q:
            try:
                q = q.decode('utf-8')
            except UnicodeDecodeError:
                q = q.decode('gb18030')
            q = q.encode('utf-8')
            now, list_limit, offset = limit_offset(n, PAGE_LIMIT)
            zsite_list, total = search(q, offset, list_limit)
            page = str(Page(
                '/q-%%s/%s' % quote(q).replace("%","%%"),
                total,
                now,
                PAGE_LIMIT
            ))
            self.render(
                q=q,
                zsite_list=zsite_list,
                total=total,
                page=page,
            )
