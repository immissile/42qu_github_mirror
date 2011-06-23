#!/usr/bin/env python
#coding:utf-8


import _handler
from _urlmap import urlmap
from model.user_mail import user_id_by_mail, mail_by_user_id
from model.user_auth import user_password_sha256, sha256
from model.api_client import api_session_new
from model.api_user import json_info
from model.follow import follow_id_list_by_from_id, follow_id_list_by_to_id, follow_count_by_to_id, follow_count_by_from_id, follow_rm, follow_new

@urlmap('/user/info/mail')
class InfoMail(_handler.ApiBase):
    def get(self):
        mail = self.get_argument('mail')
        user_id = user_id_by_mail(mail)
        data = json_info(user_id)
        self.finish(data)


@urlmap('/user/auth/login')
class Login(_handler.ApiSignBase):
    def get(self):
        user_id = self.get_argument('user_id')
        auth = self.get_argument('token')
        client_id = self.get_argument('client_id')
        password = user_password_sha256(user_id)
        if not password:
            return self.finish('{}')

        if auth != sha256(mail_by_user_id(user_id)+password).hexdigest():
            return self.finish('{}')

        self.finish({
            'S':api_session_new(client_id, user_id)
        })

@urlmap('/user/info/id')
class InfoId(_handler.ApiBase):
    def get(self):
        user_id = self.get_argument('user_id')
        data = json_info(user_id)
        self.finish(data)

@urlmap('/user/follower')
class UserFollower(_handler.ApiBase):
    def get(self):
        user_id = self.get_argument('user_id')
        limit = int(self.get_argument('limit',25))
        offset = int(self.get_argument('offset',0))
        if limit > 100:
            limit = 100
        ids = follow_id_list_by_to_id(user_id,limit,offset)
        total_num = follow_count_by_to_id(user_id)
        data = {}
        data['follower_list'] = list(ids)
        data['total_num'] = total_num
        self.finish(data)

@urlmap('/user/following')
class UserFollowing(_handler.ApiBase):
    def get(self):
        user_id = self.get_argument('user_id')
        ids = follow_id_list_by_from_id(user_id)
        total_num = follow_count_by_from_id(user_id)
        data = {}
        data['total_num'] = total_num
        data['following_list'] = list(ids)
        self.finish(data)

@urlmap('/user/following')
class UserFollowing(_handler.ApiBase):
    def get(self):
        user_id = self.get_argument('user_id')
        ids = follow_id_list_by_from_id(user_id)
        total_num = follow_count_by_from_id(user_id)
        data = {}
        data['total_num'] = total_num
        data['following_list'] = list(ids)
        self.finish(data)

@urlmap('/user/follow')
class UserFollow(_handler.LoginBase):
    def get(self):
        user_id = self.current_user_id
        follow_id = self.get_argument('to_id')
        res = follow_new(user_id, follow_id)
        self.finish({
                'status':res
                })
@urlmap('/user/follow/rm')
class UserFollowRm(_handler.LoginBase):
    def get(self):
        user_id = self.current_user_id
        unfollow_id = self.get_argument('to_id')
        res = follow_rm(user_id, unfollow_id)
        self.finish({
                'status':res
                })






