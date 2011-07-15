#coding:utf-8
import _env
from zweb.orm import ormiter

def sitemap_zsite():
    from model.zsite import Zsite
    for i in ormiter(Zsite):
        yield "http:%s"%(
            i.link
        )

def sitemap_po():
    from model.po import Po
    for i in ormiter(Po):
        yield "http:%s"%(
            i.link
        )

