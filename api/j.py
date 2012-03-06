#!/usr/bin/env python
#coding:utf-8
from _handler import Base
from _urlmap import urlmap

from yajl import dumps
from model.zsite_url import zsite_by_domain
from model.zsite_url import url_or_id, name_dict_url_dict_by_zsite_id_list
from model.follow import follow_name_dict_url_dict_by_from_id_cid, follow_reply_name_dict_url_dict_by_from_id_cid
from zkit.at_match import zsite_by_key
from model.ico import ico_url_bind_with_default
from model.career import career_bind
from model.cid import CID_USER
from model.zsite import Zsite
from model.user_session import user_id_by_session
from zweb.json import jsonp

def _get(self, func):
    key = self.get_argument('q', None)
    user_id = self.current_user_id
    result = []
    if user_id:
        name_dict, url_dict = func(user_id)
        id_list = zsite_by_key(key, name_dict, url_dict, 7)
        zsite_list = Zsite.mc_get_list(id_list)
        ico_url_bind_with_default(zsite_list)
        career_bind(zsite_list)

        for i in zsite_list:
            li = (i.name, ','.join(i.career), url_or_id(i.id), i.ico)
            result.append(li)
    #print result
    self.finish(jsonp(self, dumps(result)))

@urlmap('/j/at/reply/(\d+)')
class AtReply(Base):
    def get(self, id):
        return _get(
            self,
            lambda user_id:follow_reply_name_dict_url_dict_by_from_id_cid(user_id, id)
        )

@urlmap('/j/at')
class At(Base):
    def get(self):
        return _get(self, lambda user_id:follow_name_dict_url_dict_by_from_id_cid(user_id, CID_USER))


from model.autocomplete_query import autocomplete

@urlmap('/tip')
class Tip(Base):

    def get(self):
        q = self.get_argument('q',None)
        if q:
            result = autocomplete(q)
            result = dumps(result) 
        else:
            result = []

        self.finish(jsonp(self,result))
        
    post = get
