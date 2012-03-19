#coding:utf-8
from ctrl._urlmap_istarsea.j import urlmap
from _handler import Base
from yajl import dumps
from model.ico import ico_url_bind_with_default , ico_url_with_default
from model.career import career_current
from model.zsite import Zsite
from model.zsite_url import id_by_url
from model.follow import follow_get
from model.cid import CID_USER
from model.motto import motto_get

@urlmap('/j/hero/(.+)')
class HeroJson(Base):
    def get(self, id):
        current_user_id = self.current_user_id
        result = None
        if not id.isdigit():
            id = id_by_url(id)
        if id:
            id = int(id)
        if not id or current_user_id == id:
            return self.finish('null')

        zsite = Zsite.mc_get(id)
        if zsite:
            career = career_current(id)
            career = filter(bool, career)
            current_user_id = self.current_user_id
            if current_user_id != id:
                if follow_get(current_user_id, id):
                    word = '淡忘'
                else:
                    word = '关注'
                result = [zsite.name, ' , '.join(career), ico_url_with_default(id), zsite.link, zsite.id, word, motto_get(zsite.id)]
        return self.finish(dumps(result))

