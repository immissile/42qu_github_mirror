#!/usr/bin/env python
# -*- coding: utf-8 -*-
import _env
from zkit.single_process import single_process
from model.oauth import OauthToken
from model.oauth_verify import oauth_verify_by_oauth_id


@single_process
def oauth_verify():
    c = OauthToken.raw_sql('select id from oauth_token order by id')
    for id, in c.fetchall():
        oauth_verify_by_oauth_id(id)



if __name__ == '__main__':
    oauth_verify()
