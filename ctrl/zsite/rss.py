# -*- coding: utf-8 -*-
from model.zsite import Zsite
from model.po import po_view_list, Po
from model.zsite_tag import tag_by_po_id
from model.career import career_current
from model.cid import CID_NOTE
from model.ico import ico_url
from config import SITE_DOMAIN
from model.txt import txt_get
from ctrl._urlmap.zsite import urlmap
from _handler import ZsiteBase
from time import gmtime, strftime, time
from model.cid import CID_NOTE, CID_SITE
from cgi import escape
from model.motto import motto_get
from model.zsite_url import host
from model.site_po import feed_po_list_by_zsite_id

def format_rfc822_data(sec):
    return strftime('%a, %d %b %Y %H:%M:%S +0800', gmtime(sec))


@urlmap('/rss')
class Rss(ZsiteBase):
    def get(self):
        self.set_header('Content-Type', 'text/xml; charset=utf-8')

        items = []
        zsite = self.zsite
        id = zsite.id
        rss_title = '%s %s' % (zsite.name, host(id))
        rss_link = 'http:%s/rss' % zsite.link
        pubdate = time()
        rss_desc = motto_get(id)

        limit = 25
        offset = 0
        if zsite.cid == CID_SITE:
            site_po_list = feed_po_list_by_zsite_id(self.current_user_id, id, CID_NOTE, limit, offset)[0]
            po_id_list = []
            for i in site_po_list:
                po_id_list.append(i[1])
            po_list = Po.mc_get_list(po_id_list)
        else:
            po_list = po_view_list(id, CID_NOTE, False, limit, offset)

        for po in po_list:
            d = {}
            author = Zsite.get(po.user_id)
            po_title = po.name
            po_link = 'http:%s/%s' % (zsite.link, po.id)
            tag = tag_by_po_id(id, po.id)[2]
            title = [po_title]
            if tag:
                title.append('#%s#'%tag)
            d['title'] = ' '.join(title)
            d['author'] = author.name
            d['link'] = po_link
            htm = po.htm

            htm = htm.replace('class="PICR"', 'style="float:right;margin-left:14px"')\
                     .replace('class="PICL"', 'style="float:left;margin-right:14px"')\
                     .replace('class="PIC"', 'style="margin:14px auto"')

            desc = [
            """<font face="Verdana,sans-serif" size="3">
<pre style="font-family:Verdana;font-size:14px;white-space:pre-wrap;word-wrap:break-word;line-height:27px;">%s</pre>
""" % htm
            ]
            unit, title = career_current(id)
            desc.append(
                """ <div style="padding:27px 0;text-align:left;font-size:14px;float:left"><a target="_blank" href="%s">"""%author.link
            )

            ico = ico_url(id)
            if ico:
                desc.append(
                    """<img style="float:left;margin-right:28px" src="%s">"""%ico
                )

            desc.append("""<div style="line-height:32px;float:left"><div>%s</div><div style="color:#000">"""%escape(author.name))

            if unit:
                desc.append("""<div>%s</div>"""%escape(unit))

            if title:
                desc.append("""<div>%s</div>"""%escape(title))

            desc.append("""</div></div></a></div>""")
            desc.append('</font>')
            d['desc'] = ''.join(desc)
            d['pubdate'] = format_rfc822_data(po.create_time)
            items.append(d)

        self.render(
            rss_title=rss_title,
            rss_link=rss_link,
            rss_desc=rss_desc,
            pubdate=format_rfc822_data(pubdate),
            items=items,
        )
