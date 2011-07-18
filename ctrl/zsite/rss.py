# -*- coding: utf-8 -*-
from model.zsite import Zsite
from model.po_show import po_show_list
from model.po import po_view_list
from model.user_mail import mail_by_user_id
from model.zsite_tag import tag_by_po_id
from model.career import career_current
from model.po_pic import pic_list
from config import SITE_DOMAIN
from model.txt import txt_get
from ctrl._urlmap.zsite import urlmap
from _handler import ZsiteBase 
from time import gmtime, strftime, time

def format_rfc822_data(sec): 
    return strftime("%a, %d %b %Y %H:%M:%S +0800", gmtime(sec))

#@urlmap('/rss/human')
#class RssHuman(ZsiteBase):
#    def get(self):
#        items = []
#        rss_title = '42区资讯'
#        rss_link = 'http://%s/rss/human' % SITE_DOMAIN
#        pubdate = time()
#        rss_desc = '42qu %s 资讯' % format_rfc822_data(pubdate)
#
#        for po in po_show_list(0, 'id', 25, 0):
#            d = {}
#            author = Zsite.get(po.user_id)
#            po_title = po.name_
#            po_link = 'http://%s/%s' % (SITE_DOMAIN, po.id)
#            tag = tag_by_po_id(zsite.id, po.id)
#            d['title'] = "%s | %s" % (tag, po_title)
#            d['author'] = mail_by_user_id(po.user_id)
#            d['link'] = po_link
#            txt = txt_get(po.id)
#            if len(txt) > 100:
#                txt = txt.decode('utf8')[:100] + "......"
#            desc = [
#                """<font face="Verdana,sans-serif" size="3"><pre style="font-family:Verdana;font-size:14px;white-space:pre-wrap;word-wrap:break-word;line-height:27px;">%s</pre><div style="margin:27px 0;padding:27px 0;border-top:1px dotted #ddd;border-bottom:1px solid #ddd;text-align:right;font-size:16px;">"""%(txt)
#            ]
#
#            desc.append("""<p><a href="%s">%s</a></p>"""%(author.link, author.name))
#            desc.append("""</div></font>""")
#            d['desc'] = ''.join(desc)
#            d['pubdate'] = format_rfc822_data(po.create_time)
#            items.append(d)
#
#        self.template = "_util/rss_human.htm"
#        self.render(
#            rss_title=rss_title,
#            rss_link=rss_link,
#            rss_desc=rss_desc,
#            pubdate=format_rfc822_data(pubdate),
#            items=items,
#        )

@urlmap('/rss')
class Rss(ZsiteBase):
    def get(self):
        items = []
        zsite = self.zsite
        rss_title = '%s的文章 | 42qu.com' % zsite.name
        rss_link = 'http:%s/rss' % zsite.link
        pubdate = time()
        rss_desc = '%s 的文章 | 42qu.com %s' % (zsite.name, format_rfc822_data(pubdate))
        cid = 0
        limit = 25
        offset = 0
        po_list = po_view_list(zsite.id, cid, False, limit, offset)

        for po in po_list:
            d = {}
            author = Zsite.get(po.user_id)
            po_title = po.name_
            po_link = 'http:%s/%s' % (zsite.link, po.id)
            tag = tag_by_po_id(zsite.id, po.id)[2]
            d['title'] = "%s #%s" % (po_title, tag)
            d['author'] = mail_by_user_id(po.user_id)
            d['link'] = po_link
            #if len(txt) > 100:
            #    txt = txt.decode('utf8')[:100] + "......"
            desc = [
            """<font face="Verdana,sans-serif" size="3"><pre style="font-family:Verdana;font-size:14px;white-space:pre-wrap;word-wrap:break-word;line-height:27px;">%s</pre><div style="margin:27px 0;padding:27px 0;text-align:left;font-size:16px;">"""%(po.htm)
            ]
            unit, title = career_current(zsite.id)
            desc.append("""<a href="%s">%s</a>, %s, %s"""%(author.link, author.name, unit, title))
            desc.append("</br></div></font>")
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

