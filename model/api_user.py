#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model.zsite import Zsite
from model.motto import motto
from model.ico import ico96, ico, ico_url
from model.namecard import namecard_get
from model.follow import follow_count_by_to_id, follow_count_by_from_id
from zkit.earth import place_name
from model.user_info import UserInfo

def json_info(user_id):
    user_id = int(user_id)
    user = Zsite.mc_get(user_id)
    namecard = namecard_get(user_id)
    user_info = UserInfo.get(user_id)
    data = {}
    if user_info:
        if user:
            data['cid'] = user.cid
            data['user_id'] = user_id
            data['self_intro'] = user.txt
            data['name'] = user.name
            data['ico'] = ico_url(user_id) or ''
            data['moto'] = motto.get(user_id)
            data['user_link'] = 'http:%s'%user.link
            data['sex'] = user_info.sex
            data['marry'] = user_info.marry
            data['follower_num'] = follow_count_by_to_id(user_id)
            data['following_num'] = follow_count_by_from_id(user_id)
            data['verify_state'] = user.state
            data['pic'] = ico.get(user_id)
            if namecard:
                if namecard.pid_now:
                    data['place_now_name'] = namecard.place_now
                    data['place_now'] = namecard.pid_now
            if user_info.pid_home:
                data['place_home_name'] = user_info.place_home
                data['place_home'] = user_info.pid_home
    return data
