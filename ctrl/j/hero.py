#coding:utf-8
from zkit.bot_txt import txt_wrap_by
from ctrl._urlmap.j import urlmap
from _handler import JLoginBase
from yajl import dumps
from model.ico import ico_url_bind_with_default
from model.career import career_bind
from model.zsite import Zsite
from logging import info
from model.zsite_url import id_by_url, url_or_id
from model.follow import follow_count_by_to_id, follow_get
from model.cid import CID_USER

@urlmap('/j/hero')
class HeroJson(JLoginBase):
    def post(self):
        url = self.get_argument('url', None)
        id = id_by_url(txt_wrap_by('//','.',url))
        id_list = []
        id_list.append(id)
        zsite_list = Zsite.mc_get_list(id_list)
        ico_url_bind_with_default(zsite_list)
        career_bind(zsite_list)
        result = []
        for i in zsite_list:
            if follow_get(self.current_user_id, i.id):
                word = "淡忘"
            else:
                word = "关注"
            fo_num = follow_count_by_to_id(i.id)
            result = [i.name, ','.join(i.career), i.ico, fo_num, i.id, word, url_or_id(i.id)]
        return self.finish(dumps(result))
