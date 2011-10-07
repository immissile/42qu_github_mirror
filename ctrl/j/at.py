#!/usr/bin/env python
# -*- coding: utf-8 -*-
from yajl import dumps
from ctrl._urlmap.j import urlmap
from model.zsite_url import zsite_by_domain
from _handler import JLoginBase
from model.zsite_url import url_or_id, name_dict_url_dict_by_zsite_id_list
from model.follow import follow_name_dict_url_dict_by_from_id_cid, follow_reply_name_dict_url_dict_by_from_id_cid
from zkit.at_match import zsite_by_key
from model.ico import ico_url_bind_with_default 
from model.career import career_bind
from model.cid import CID_USER
from model.zsite import Zsite 

def _post(self, name_dict, url_dict):
    key = self.get_argument('q', None)
    result = []
    
    id_list = zsite_by_key(key, name_dict, url_dict, 7)
    zsite_list = Zsite.mc_get_list(id_list)
    ico_url_bind_with_default(zsite_list)
    career_bind(zsite_list)

    for i in zsite_list:
        li = (i.name, ','.join(i.career), url_or_id(i.id), i.ico)
        result.append(li)
    
    self.finish(dumps(result))

@urlmap('/j/at/reply/(\d+)')
class AtReply(JLoginBase):
    def post(self, id):
        name_dict, url_dict = follow_reply_name_dict_url_dict_by_from_id_cid(self.current_user_id, id)
        return _post(self, name_dict, url_dict)

@urlmap('/j/at')
class At(JLoginBase):
    def post(self):
        return _post(self, *follow_name_dict_url_dict_by_from_id_cid(self.current_user_id, CID_USER))


