# -*- coding: utf-8 -*-
from _handler import Base, LoginBase, XsrfGetBase
from ctrl._urlmap.hero import urlmap
from model.zsite_show import zsite_show_list, zsite_show_count
from model.cid import CID_USER
from zkit.page import page_limit_offset
from model.zsite import Zsite
from config import SITE_DOMAIN
from model.user_school import user_school_tuple, user_school_new, user_school_search

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

SCHOOL_LINK = '/q/school/%s/%s/%s/%s'

@urlmap('/q/school')
@urlmap('/q/school/(\d+)/(\d+)/(\d+)/(\d+)')
@urlmap('/q/school/(\d+)/(\d+)/(\d+)/(\d+)-(\d+)')
class School(LoginBase):
    def get(self, id=0, year=0, degree=0, department=0, n=1):
        school_id         = self.get_argument('school_id', None)
        school_year       = self.get_argument('school_year', 0)
        school_degree     = self.get_argument('school_degree', 0)
        school_department = self.get_argument('school_department', 0)
        is_my = int(bool(self.get_argument('is_my', None) == 'on'))

        if school_id:
            if is_my:
                user_school_new(
                    self.current_user_id, 
                    school_id, school_year, school_degree,
                    school_department
                ) 
            return self.redirect(
                SCHOOL_LINK%(
                    school_id, school_year, school_degree, school_department
                )
            )
        school_tuple = user_school_tuple(self.current_user_id)
        if not id and school_tuple:
            id, school_id, school_year, school_degree, school_department, txt = school_tuple[0]           
            return self.redirect(SCHOOL_LINK%(school_id, school_year, school_degree, school_department))

        zsite_list , page = hero_page(n)
        self.render(
            zsite_list        = zsite_list        , 
            page              = page              ,
            school_data       = (   0                 ,
                                    id         , 
                                    year       ,
                                    degree     ,
                                    department ,     
                                    '' 
                                ),
            school_id         = id, 
            school_tuple      = school_tuple          ,
            result            = user_school_search(id, year, degree, department)
        )



