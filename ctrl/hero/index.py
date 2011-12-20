# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.hero import urlmap
from model.zsite_show import zsite_show_list, zsite_show_count
from model.cid import CID_USER
from zkit.page import page_limit_offset
from model.zsite import Zsite
from config import SITE_DOMAIN

def hero_page(n):
    n = int(n)
    count = zsite_show_count(CID_USER)
    page, limit, offset = page_limit_offset(
        '//hero.%s/-%%s'%SITE_DOMAIN,
        count,
        n,
        64
    )
    zsite_list = zsite_show_list(CID_USER, limit, offset)
    return zsite_list, page

@urlmap('/')
@urlmap('/-(\d+)')
class Index(Base):
    def get(self, n=1):
        zsite_list , page = hero_page(n)
        self.render(zsite_list=zsite_list, page=page)


@urlmap('/q/school')
@urlmap('/q/school/(\d+)/(\d+)/(\d+)-(\d+)')
class School(Base):
    def get(self, id=0, year=0, degree=0, n=1):
        school_id         = self.get_argument('school_id', None)
        school_year       = self.get_argument('school_year', 0)
        school_degree     = self.get_argument('school_degree', 0)
        school_department = self.get_argument('school_department', 0)
        is_my = int(bool(self.get_argument('is_my', None) == 'on'))

        if school_id:
            return self.redirect(
                '/q/school/%s/%s/%s-%s'%(
                    school_id, school_year, school_degree, school_department
                )
            )

        zsite_list , page = hero_page(n)
        self.render(
            zsite_list        = zsite_list        , 
            page              = page              ,
            school_id         = school_id         , 
            school_year       = school_year       ,
            school_degree     = school_degree     ,
            school_department = school_department ,       
        )



