#coding:utf-8
import init_env
from mysite.model.man_link import rss_id_by_man_link
from mysite.util.orm import ormiter
from mysite.model.man import Man

def sitemap_video():
    from mysite.model.video import VideoList
    for i in ormiter(VideoList):
        yield "/video/play/%s"%(
            i.id,
        )

def man_link(man_id):
    man = Man.get(man_id)
    if man:
        r = man.link
    else:
        r = ""
    return r


def sitemap_note():
    from mysite.model.note import Note
    for i in ormiter(Note):
        yield "%s/note/-%s"%(man_link(i.man_id), i.id)

def sitemap_qa():
    from mysite.model.review import Review
    for i in ormiter(Review):
        yield "%s/qa/txt/%s"%(man_link(i.from_id),i.to_id)

def sitemap_user():
    from mysite.model.man import Man
    for i in ormiter(Man):
        link = i.link
        yield link
#        if rss_id_by_man_link(i.id):
#            yield "%s/feed"%link

#
#
#def sitemap_gadget_source():
#    from mysite.model.gadget import GadgetSource
#    from mysite.model.rss import RssOwner, RssUser
#    from mysite.model.user import User
#    for source in ormiter(GadgetSource, "see=1 and cid!=6"):
#        rss_id = source.rid
#        rss_owner = RssOwner.get(rss_id)
#
#        user = None
#
#        if rss_owner:
#            user = User.mc_get(rss_owner.user_id)
#        else:
#            l = RssUser.get(rss_id=rss_id)
#            if l:
#                user = User.mc_get(l.user_id)
#        if user is not None:
#            yield "%s/t/%s"%(user.link, source.id)
#
#def sitemap_cell():
#    from mysite.model.cell import Cell
#    for cell in ormiter(Cell):
#        yield cell.link
