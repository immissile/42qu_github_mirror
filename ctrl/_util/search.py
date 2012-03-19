from urllib import quote
from zkit.page import limit_offset, Page

PAGE_LIMIT = 64

def search_get(self, n=1):
    page_limit = getattr(self, 'PAGE_LIMIT', PAGE_LIMIT)
    q = self.get_argument('q', '')
    if q:
        try:
            q = q.decode('utf-8')
        except UnicodeDecodeError:
            q = q.decode('gb18030')

        q = q.encode('utf-8')
        now, list_limit, offset = limit_offset(
            n,
            page_limit
        )

        zsite_list, total = self.search(q, offset, list_limit)
        page = str(Page(
            getattr(self, 'link', '/q-%%s?q=%s') % quote(q).replace('%', '%%'),
            total,
            now,
            page_limit
        ))

        self.render(
            q=q,
            page_list=zsite_list,
            total=total,
            page=page,
        )
    else:
        self.render(q=None)

